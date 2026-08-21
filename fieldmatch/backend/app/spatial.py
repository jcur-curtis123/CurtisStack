"""
Parcel loading and point-in-polygon lookup.

load_parcels() uses a real backend/data/*.shp or *.geojson if present,
otherwise falls back to the bundled synthetic demo dataset so the app
runs out of the box. See backend/README.md for swapping in real
municipal parcel data.

find_containing_feature() uses the GeoDataFrame's spatial index
(gdf.sindex) to narrow candidates before doing exact geometry
containment checks, instead of scanning every row. This matters once a
real municipal parcels shapefile (tens of thousands of features)
replaces the demo data.
"""

import os
from typing import Optional

import geopandas as gpd
from shapely.geometry import Point

# Resolve relative to this file, not the process's cwd -- the quickstart
# runs uvicorn from inside backend/, which made the old cwd-relative
# "backend/data/parcels.shp" resolve to backend/backend/data/parcels.shp
# and silently fall back to demo data even with a real shapefile present.
APP_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(APP_DIR)
DEMO_DATA_PATH = os.path.join(APP_DIR, "data", "sample_parcels.geojson")
REAL_DATA_DIR = os.path.join(BACKEND_DIR, "data")

# Real assessor exports use all kinds of column names for the same
# field. Matched case-insensitively so backend/README.md's "drop your
# shapefile in and go" promise actually holds for common county/GIS
# export conventions, not just the bundled demo file's exact names.
FIELD_ALIASES = {
    "parcel_id": ["maplot", "map_lot", "parcel_id", "parcelid", "pid", "gisid"],
    "zone": ["zone", "zoning", "zone_code", "zonedesc"],
    "lot_sqft": ["lotarea", "lot_area", "lot_sqft", "sqft", "shape_area"],
    "growth_area": ["growth_area", "growtharea", "in_growth"],
    "shoreland": ["shoreland", "shoreland_zone", "in_shoreland"],
}


def _find_column(columns, aliases) -> Optional[str]:
    lower = {c.lower(): c for c in columns}
    for alias in aliases:
        if alias in lower:
            return lower[alias]
    return None


def _to_float(value) -> Optional[float]:
    try:
        return None if value is None else float(value)
    except (TypeError, ValueError):
        return None


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, (int, float)):
        return bool(value)
    return str(value).strip().lower() in ("y", "yes", "true", "1", "t")


def load_parcels() -> tuple:
    """Return (gdf, is_demo_data)."""
    if os.path.isdir(REAL_DATA_DIR):
        for fname in sorted(os.listdir(REAL_DATA_DIR)):
            if fname.lower().endswith((".shp", ".geojson", ".json")):
                gdf = gpd.read_file(os.path.join(REAL_DATA_DIR, fname))
                if gdf.crs is not None:
                    try:
                        if gdf.crs.to_epsg() != 4326:
                            gdf = gdf.to_crs(epsg=4326)
                    except Exception:
                        gdf = gdf.to_crs(epsg=4326)
                return gdf, False

    gdf = gpd.read_file(DEMO_DATA_PATH)
    return gdf, True


def find_containing_feature(gdf, lon: float, lat: float):
    """Return the attributes (as a dict) of the parcel containing (lon, lat),
    or None if no parcel matches. Column names are normalized to the
    subset of fields the rest of the app expects (parcel_id, zone,
    lot_sqft, growth_area, shoreland), falling back to sensible defaults
    when a real shapefile uses different field names.
    """
    if gdf is None or len(gdf) == 0:
        return None

    pt = Point(lon, lat)

    # Narrow candidates via the spatial index, then confirm with an exact
    # containment test -- avoids a full linear scan on large parcel sets.
    try:
        candidate_idx = list(gdf.sindex.query(pt, predicate="intersects"))
    except Exception:
        candidate_idx = list(range(len(gdf)))
    candidates = gdf.iloc[candidate_idx] if candidate_idx else gdf.iloc[0:0]

    id_col = _find_column(gdf.columns, FIELD_ALIASES["parcel_id"])
    zone_col = _find_column(gdf.columns, FIELD_ALIASES["zone"])
    area_col = _find_column(gdf.columns, FIELD_ALIASES["lot_sqft"])
    growth_col = _find_column(gdf.columns, FIELD_ALIASES["growth_area"])
    shoreland_col = _find_column(gdf.columns, FIELD_ALIASES["shoreland"])

    for _, row in candidates.iterrows():
        geom = row.geometry
        if geom is None:
            continue
        if geom.contains(pt) or geom.touches(pt) or geom.intersects(pt):
            return {
                "parcel_id": str(row[id_col]) if id_col and row[id_col] is not None else "unknown",
                "zone": row[zone_col] if zone_col else None,
                "lot_sqft": _to_float(row[area_col]) if area_col else None,
                "growth_area": _to_bool(row[growth_col]) if growth_col else False,
                "shoreland": _to_bool(row[shoreland_col]) if shoreland_col else False,
            }

    return None
