from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.geocode import geocode_address
from app.spatial import load_parcels, find_containing_feature
from app.zoning import assess_duplex_eligibility

app = FastAPI(title="FieldMatch")

# Allow the Vite dev server (default port 5173) and CRA-style 3000 to
# call this API from the browser. Tighten this to your real frontend
# origin(s) before deploying anywhere public.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

PARCELS, USING_DEMO_DATA = load_parcels()


class AnalyzeRequest(BaseModel):
    address: str
    question: str = ""


@app.get("/api/health")
def health():
    return {"ok": True, "demo_data": USING_DEMO_DATA, "parcel_count": len(PARCELS)}


@app.post("/api/analyze")
def analyze(req: AnalyzeRequest):
    geo = geocode_address(req.address)
    parcel = find_containing_feature(PARCELS, geo["lon"], geo["lat"])

    if parcel is None:
        return {
            "address": req.address,
            "geocoded": geo,
            "parcel": None,
            "answer": (
                "No parcel found at this location."
                + (" (using bundled demo data covering downtown Portland, ME only)" if USING_DEMO_DATA else "")
            ),
            "confidence": 0.2,
        }

    zoning = assess_duplex_eligibility(
        zone=parcel["zone"],
        lot_area_sqft=parcel["lot_sqft"],
        growth_area=parcel["growth_area"],
        shoreland=parcel["shoreland"],
    )

    if zoning["eligible"] is True:
        answer = f"Likely yes. {zoning['basis']}"
    elif zoning["eligible"] is False:
        answer = f"Likely not by right. {zoning['basis']}"
    else:
        answer = zoning["basis"]

    confidence = zoning["confidence"]
    if not geo["matched"]:
        confidence = min(confidence, 0.4)

    return {
        "address": req.address,
        "question": req.question,
        "geocoded": geo,
        "parcel": {
            "parcel_id": parcel["parcel_id"],
            "zone": parcel["zone"],
            "lot_sqft": parcel["lot_sqft"],
            "growth_area": parcel["growth_area"],
            "shoreland": parcel["shoreland"],
        },
        "eligibility": zoning,
        "answer": answer,
        "confidence": round(confidence, 2),
        "demo_data": USING_DEMO_DATA,
    }
