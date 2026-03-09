import cv2
import numpy as np
from .models import DetectedObject, Point


def detect_panel(img_gray):
    edges = cv2.Canny(img_gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    best = None
    best_area = 0

    for c in contours:
        x,y,w,h = cv2.boundingRect(c)
        area = w * h

        # Typical panel proportions
        if area < 1500:
            continue
        if w/h < 0.5 or w/h > 2.5:
            continue

        if area > best_area:
            best = (x,y,w,h)
            best_area = area

    if not best:
        return None

    x,y,w,h = best
    return DetectedObject(
        id="panel_1",
        type="panel",
        center=Point(x=x+w/2, y=y+h/2),
        bbox=[x,y,w,h],
        confidence=0.8
    )
