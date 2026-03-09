from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.wiring.models import OptimizeRequest, OptimizeResponse, DetectionResult
from backend.wiring.route import optimize
from backend.wiring.detect import detect_from_image

app = FastAPI()

# -------------------
# CORS (frontend access)
# -------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------
# Health check
# -------------------
@app.get("/")
def health():
    return {"status": "ok"}

# -------------------
# AUTO-DETECT ENDPOINT
# -------------------
@app.post("/detect", response_model=DetectionResult)
async def detect_api(file: UploadFile = File(...)):
    image_bytes = await file.read()
    return detect_from_image(image_bytes)

# -------------------
# OPTIMIZATION ENDPOINT
# -------------------
@app.post("/optimize", response_model=OptimizeResponse)
def optimize_api(req: OptimizeRequest):
    return optimize(req)
