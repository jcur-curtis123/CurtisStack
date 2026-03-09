import cv2
import numpy as np

def detect_wall_openings(wall_mask, min_width=25, max_width=70):
    """
    Detect gaps in walls that represent doors/openings.

    wall_mask: uint8 image (255 = wall, 0 = empty)
    returns: list of opening contours
    """

    # Invert: walls -> 0, empty -> 255
    inv = 255 - wall_mask

    # Distance transform highlights open regions
    dist = cv2.distanceTransform(inv, cv2.DIST_L2, 5)

    # Threshold for potential door-sized gaps
    gap_mask = np.zeros_like(dist, dtype=np.uint8)
    gap_mask[(dist > min_width) & (dist < max_width)] = 255

    gap_mask = gap_mask.astype(np.uint8)

    contours, _ = cv2.findContours(
        gap_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    openings = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if min_width <= w <= max_width or min_width <= h <= max_width:
            openings.append(cnt)

    return openings
