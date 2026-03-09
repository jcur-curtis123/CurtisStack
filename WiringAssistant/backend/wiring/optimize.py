import cv2
import base64
import numpy as np
from utils.cost_map import build_cost_grid
from utils.routing import astar_manhattan

def decode_mask(b64):
    data = base64.b64decode(b64)
    arr = np.frombuffer(data, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_GRAYSCALE)

def optimize_routes(payload):
    wall_mask = decode_mask(payload["wall_mask"])
    doors = [np.array(d, dtype=np.int32) for d in payload["doors"]]

    cost_grid = build_cost_grid(wall_mask, doors)

    panel = payload["panel"]
    outlets = payload["outlets"]

    routes = []
    for outlet in outlets:
        path = astar_manhattan(
            cost_grid,
            (panel["x"], panel["y"]),
            (outlet["x"], outlet["y"])
        )
        routes.append(path)

    return routes
