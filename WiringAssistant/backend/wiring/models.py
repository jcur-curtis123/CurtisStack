from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


# -------------------------
# Basic geometry primitives
# -------------------------

class Point(BaseModel):
    x: float
    y: float


class Polygon(BaseModel):
    points: List[Point]


# -------------------------
# Detection layer
# -------------------------

class DetectedObject(BaseModel):
    """
    Generic detected object on the plan.
    """
    id: str
    type: Literal[
        "panel",
        "outlet",
        "switch",
        "light",
        "gfci",
        "door",
        "unknown",
    ]
    center: Point
    bbox: Optional[List[int]] = None  # [x, y, w, h]
    confidence: float = 1.0


class DetectionResult(BaseModel):
    """
    Output of the detection stage.
    """
    width: int
    height: int
    objects: List[DetectedObject] = Field(default_factory=list)
    walls: List[Polygon] = Field(default_factory=list)
    wall_mask_png_base64: Optional[str] = None


# -------------------------
# Optimization input
# -------------------------

class OptimizeRequest(BaseModel):
    """
    Request payload for routing + circuit optimization.
    """
    width: int
    height: int

    panel_id: str
    outlet_ids: List[str]

    objects: List[DetectedObject]

    wall_mask_png_base64: str

    # --- Circuit grouping controls ---
    auto_group_circuits: bool = True
    max_outlets_per_circuit: int = 6

    # Optional manual override:
    # [
    #   ["outlet_1", "outlet_2"],
    #   ["outlet_3"]
    # ]
    circuit_outlet_ids: Optional[List[List[str]]] = None


# -------------------------
# Routing output
# -------------------------

class Route(BaseModel):
    """
    A single routed polyline segment.
    """
    points: List[Point]

    # NEW: trunk vs branch labeling
    kind: Literal["trunk", "branch"] = "branch"


class CircuitRoute(BaseModel):
    """
    All routes belonging to a single circuit.
    """
    id: str
    outlet_ids: List[str]
    routes: List[Route]
    total_length_px: float


class OptimizeResponse(BaseModel):
    """
    Full optimization response.
    """
    # Flattened routes (easy for frontend rendering)
    routes: List[Route]

    total_length_px: float

    # Structured, electrician-grade output
    circuits: List[CircuitRoute] = Field(default_factory=list)
