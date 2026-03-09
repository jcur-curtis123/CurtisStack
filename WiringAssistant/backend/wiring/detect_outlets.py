import cv2
import numpy as np
from typing import List
from .models import DetectedObject, Point


def detect_outlets(img_gray, min_area=80, max_area=600):
    """
    Detect outlet-like symbols using blob detection.
    """
    # Emphasize symbols
    _, bw = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3,3), np.uint8)
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(bw, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    outlets: List[DetectedObject] = []
    idx = 1

    for c in contours:
        area = cv2.contourArea(c)
        if not (min_area <= area <= max_area):
            continue

        x, y, w, h = cv2.boundingRect(c)
        cx = x + w / 2
        cy = y + h / 2

        outlets.append(
            DetectedObject(
                id=f"outlet_{idx}",
                type="outlet",
                center=Point(x=cx, y=cy),
                bbox=[x,y,w,h],
                confidence=0.6
            )
        )
        idx += 1

    return outlets
