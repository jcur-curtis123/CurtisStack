import base64
from io import BytesIO
from PIL import Image
import numpy as np

def pil_to_b64_png(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def b64_png_to_np(b64: str) -> np.ndarray:
    data = base64.b64decode(b64)
    img = Image.open(BytesIO(data)).convert("L")
    return np.array(img)

def np_to_b64_png(gray: np.ndarray) -> str:
    img = Image.fromarray(gray.astype("uint8"))
    return pil_to_b64_png(img)
