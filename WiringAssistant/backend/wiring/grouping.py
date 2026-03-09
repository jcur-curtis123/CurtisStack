from __future__ import annotations
from typing import List, Dict, Tuple, Optional
import math

from .models import DetectedObject, Point


def _dist(a: Point, b: Point) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def _angle_from(panel: Point, p: Point) -> float:
    return math.atan2(p.y - panel.y, p.x - panel.x)


def group_outlets_auto(
    panel: DetectedObject,
    outlets: List[DetectedObject],
    max_outlets_per_circuit: int = 6,
    max_radius_jump_px: float = 220.0,
    max_pair_distance_px: float = 600.0,
) -> List[List[str]]:
    """
    Heuristic circuit grouping (fast + works well for typical floor plans):
    1) Sort outlets by angle around panel (sweeping)
    2) Greedily chunk into circuits of size max_outlets_per_circuit
    3) Split early if we see a big radius jump (usually means different area/room)
    4) Safety split if outlets inside a circuit are too far apart

    Returns: List of groups, each group is a list of outlet IDs.
    """
    if max_outlets_per_circuit < 1:
        max_outlets_per_circuit = 1

    if not outlets:
        return []

    # Create polar features around panel
    items = []
    for o in outlets:
        ang = _angle_from(panel.center, o.center)
        r = _dist(panel.center, o.center)
        items.append((ang, r, o))

    # Sort by angle, then radius
    items.sort(key=lambda t: (t[0], t[1]))

    groups: List[List[DetectedObject]] = []
    cur: List[DetectedObject] = []
    last_r: Optional[float] = None

    for _, r, o in items:
        start_new = False

        if not cur:
            start_new = False
        else:
            if len(cur) >= max_outlets_per_circuit:
                start_new = True
            elif last_r is not None and abs(r - last_r) > max_radius_jump_px:
                # Sudden jump in radius: likely different region
                start_new = True

        if start_new:
            groups.append(cur)
            cur = []

        cur.append(o)
        last_r = r

    if cur:
        groups.append(cur)

    # Safety split groups if they contain far-apart outlets (prevents silly groupings)
    final_groups: List[List[str]] = []
    for g in groups:
        if len(g) <= 1:
            final_groups.append([x.id for x in g])
            continue

        # Compute max pair distance
        max_d = 0.0
        for i in range(len(g)):
            for j in range(i + 1, len(g)):
                d = _dist(g[i].center, g[j].center)
                if d > max_d:
                    max_d = d

        if max_d <= max_pair_distance_px:
            final_groups.append([x.id for x in g])
        else:
            # Split by nearest-to-panel ordering into chunks
            g_sorted = sorted(g, key=lambda x: _dist(panel.center, x.center))
            for i in range(0, len(g_sorted), max_outlets_per_circuit):
                final_groups.append([x.id for x in g_sorted[i:i + max_outlets_per_circuit]])

    # Remove any empty groups
    final_groups = [g for g in final_groups if g]
    return final_groups
