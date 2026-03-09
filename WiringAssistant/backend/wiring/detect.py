import cv2
import base64
import numpy as np

from backend.wiring.models import DetectionResult
from backend.wiring.image_utils import preprocess_image, detect_walls
from backend.wiring.detect_outlets import detect_outlets
from backend.wiring.detect_panel import detect_panel


def encode_mask(mask: np.ndarray) -> str:
    _, buf = cv2.imencode(".png", mask)
    return base64.b64encode(buf).decode("utf-8")


def detect_from_image(image_bytes: bytes) -> DetectionResult:
    # Decode uploaded image
    arr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Invalid image upload")

    gray = preprocess_image(img)

    # Walls
    wall_mask = detect_walls(gray)

    # Symbols
    panel = detect_panel(gray)
    outlets = detect_outlets(gray)

    objects = []
    if panel:
        objects.append(panel)
    objects.extend(outlets)

    return DetectionResult(
        width=img.shape[1],
        height=img.shape[0],
        objects=objects,
        wall_mask_png_base64=encode_mask(wall_mask),
    )
