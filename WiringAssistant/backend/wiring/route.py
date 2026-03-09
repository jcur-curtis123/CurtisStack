from __future__ import annotations
from typing import Dict, List, Tuple
import math
import numpy as np
import cv2

from .models import OptimizeRequest, OptimizeResponse, Route, Point, DetectedObject, CircuitRoute
from .utils import b64_png_to_np
from .grouping import group_outlets_auto
from .trunk_branch import label_trunk_and_branches


def _downsample_mask(mask: np.ndarray, max_dim: int = 512) -> Tuple[np.ndarray, float]:
    h, w = mask.shape[:2]
    scale = min(max_dim / max(h, w), 1.0)
    if scale == 1.0:
        return (mask > 0).astype(np.uint8), 1.0
    new_w = int(w * scale)
    new_h = int(h * scale)
    small = cv2.resize(mask, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
    return (small > 0).astype(np.uint8), scale


def _build_cost_grid(blocked: np.ndarray) -> np.ndarray:
    # NOTE: This is your existing “hug walls” cost map.
    free = 1 - blocked
    dist = cv2.distanceTransform(free.astype(np.uint8), cv2.DIST_L2, 3)
    dist = dist / (dist.max() + 1e-6)
    base = np.ones_like(dist, dtype=np.float32)

    # Prefer routing near walls (lower cost near walls, higher cost in open areas)
    cost = base + 2.5 * dist
    cost[blocked > 0] = np.inf
    return cost


def _neighbors(p):
    x, y = p
    # Keep your neighbors; you can switch to Manhattan-only later when you do bend penalties
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
        yield x + dx, y + dy


def _heuristic(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def astar(cost: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int]):
    h, w = cost.shape
    import heapq

    openh = []
    heapq.heappush(openh, (0.0, start))
    came = {}
    g = {start: 0.0}

    while openh:
        _, cur = heapq.heappop(openh)

        if cur == goal:
            path = [cur]
            while cur in came:
                cur = came[cur]
                path.append(cur)
            path.reverse()
            return path, g[goal]

        for nx, ny in _neighbors(cur):
            if nx < 0 or ny < 0 or nx >= w or ny >= h:
                continue
            c = cost[ny, nx]
            if not np.isfinite(c):
                continue

            step = math.hypot(nx - cur[0], ny - cur[1]) * c
            ng = g[cur] + step
            nb = (nx, ny)

            if ng < g.get(nb, float("inf")):
                g[nb] = ng
                came[nb] = cur
                f = ng + _heuristic(nb, goal)
                heapq.heappush(openh, (f, nb))

    return None, float("inf")


def _to_grid(pt: Point, scale: float) -> Tuple[int, int]:
    return (int(round(pt.x * scale)), int(round(pt.y * scale)))


def _from_grid(p: Tuple[int, int], scale: float) -> Point:
    return Point(x=float(p[0] / scale), y=float(p[1] / scale))


def _mst(n: int, dist: np.ndarray) -> List[Tuple[int, int]]:
    """
    Prim-like MST on fully-connected graph using pairwise distances.
    Node 0 is the panel.
    """
    in_mst = [False] * n
    in_mst[0] = True
    edges = []

    for _ in range(n - 1):
        best_i, best_j, best_d = None, None, float("inf")
        for i in range(n):
            if not in_mst[i]:
                continue
            for j in range(n):
                if in_mst[j]:
                    continue
                d = float(dist[i, j])
                if d < best_d:
                    best_i, best_j, best_d = i, j, d

        if best_i is None:
            break

        in_mst[best_j] = True
        edges.append((best_i, best_j))

    return edges

def _routes_for_points(cost: np.ndarray, pts: List[Point], scale: float):
    """
    Given points [panel] + outlets, compute MST routes,
    then label trunk vs branch.
    """
    grid_pts = [_to_grid(p, scale=scale) for p in pts]
    n = len(grid_pts)

    dist = np.full((n, n), np.inf, dtype=np.float32)
    paths = {}

    for i in range(n):
        for j in range(i + 1, n):
            path, d = astar(cost, grid_pts[i], grid_pts[j])
            dist[i, j] = dist[j, i] = d
            paths[(i, j)] = path
            paths[(j, i)] = path[::-1] if path else None

    edges = _mst(n, dist)

    # 🔥 NEW: label trunk vs branch
    edge_labels = label_trunk_and_branches(edges, n, panel_index=0)

    routes: List[Route] = []
    total = 0.0

    for i, j in edges:
        path = paths.get((i, j))
        if not path:
            continue

        total += float(dist[i, j])
        kind = edge_labels.get((i, j), "branch")

        pts_out = [_from_grid(p, scale=scale) for p in path[::2]]

        routes.append(
            Route(
                points=pts_out,
                kind=kind
            )
        )

    return routes, total

def optimize_routes(req: OptimizeRequest) -> OptimizeResponse:
    # Decode wall mask
    mask = b64_png_to_np(req.wall_mask_png_base64)

    # Downsample for routing speed
    blocked_small, scale = _downsample_mask(mask, max_dim=520)

    # Build routing cost grid
    cost = _build_cost_grid(blocked_small)

    # Index objects by id
    obj_by_id: Dict[str, DetectedObject] = {o.id: o for o in req.objects}

    # Get panel
    panel = obj_by_id.get(req.panel_id)
    if panel is None:
        raise ValueError(f"panel_id '{req.panel_id}' not found")

    # Get outlets
    outlets: List[DetectedObject] = []
    for oid in req.outlet_ids:
        if oid in obj_by_id:
            outlets.append(obj_by_id[oid])

    if not outlets:
        return OptimizeResponse(routes=[], total_length_px=0.0, circuits=[])

    # -------------------------
    # Circuit grouping
    # -------------------------
    if req.circuit_outlet_ids:
        circuit_groups = req.circuit_outlet_ids
    elif req.auto_group_circuits:
        circuit_groups = group_outlets_auto(
            panel=panel,
            outlets=outlets,
            max_outlets_per_circuit=req.max_outlets_per_circuit,
        )
    else:
        circuit_groups = [[o.id for o in outlets]]

    all_routes: List[Route] = []
    all_circuits: List[CircuitRoute] = []
    total_length = 0.0

    # -------------------------
    # Route each circuit
    # -------------------------
    for idx, outlet_ids in enumerate(circuit_groups):
        group_outlets = [obj_by_id[o] for o in outlet_ids if o in obj_by_id]
        if not group_outlets:
            continue

        pts = [panel.center] + [o.center for o in group_outlets]

        routes, length = _routes_for_points(cost, pts, scale)

        circuit = CircuitRoute(
            id=f"C{idx+1}",
            outlet_ids=[o.id for o in group_outlets],
            routes=routes,
            total_length_px=float(length),
        )

        all_routes.extend(routes)
        all_circuits.append(circuit)
        total_length += float(length)

    return OptimizeResponse(
        routes=all_routes,
        total_length_px=total_length,
        circuits=all_circuits,
    )
# --- FastAPI entrypoint (MUST be last) ---
def optimize(req: OptimizeRequest) -> OptimizeResponse:
    return optimize_routes(req)
