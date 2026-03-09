import cv2
import numpy as np

def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    return blur

def detect_walls(img):
    edges = cv2.Canny(img, 50, 150)
    kernel = np.ones((5,5), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)

    wall_mask = np.zeros_like(edges)
    wall_mask[edges > 0] = 255
    return wall_mask

def wall_distance_transform(wall_mask):
    # walls=255 → invert so empty space expands
    inv = 255 - wall_mask
    return cv2.distanceTransform(inv, cv2.DIST_L2, 5)
