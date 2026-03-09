import cv2
import numpy as np
from ..wiring.image_utils import wall_distance_transform

WALL_COST = 1e6
DOOR_COST = 1
FREE_COST = 1

def build_cost_grid(wall_mask, openings):
    """
    Builds a cost grid for routing:
    - walls are nearly infinite cost
    - doors are cheap portals
    - wall-adjacent paths are preferred
    """

    h, w = wall_mask.shape
    cost = np.full((h, w), FREE_COST, dtype=np.float32)

    # Walls
    cost[wall_mask == 255] = WALL_COST

    # Doors / openings
    for cnt in openings:
        cv2.fillPoly(cost, [cnt], DOOR_COST)

    # Wall hugging preference
    wall_dist = wall_distance_transform(wall_mask)
    cost += np.clip(wall_dist * 0.5, 0, 50)

    return cost
