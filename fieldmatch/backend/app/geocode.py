"""
Address -> (lon, lat) geocoding.

Uses OpenStreetMap's Nominatim public API (no API key required). Nominatim's
usage policy requires a descriptive User-Agent and a max of ~1 request/sec,
which is fine for this single-lookup-per-request use case. Swap in a paid
geocoder (Google, Mapbox, Census) here if you need higher volume or better
accuracy — the rest of the app only depends on this returning (lon, lat).
"""

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "FieldMatch/0.1 (parcel-lookup demo; contact: set-your-email-here)"

# Used only if geocoding fails (offline sandbox, network hiccup, no match) —
# keeps the demo usable end to end rather than hard-failing.
FALLBACK_LON, FALLBACK_LAT = -70.258, 43.658  # downtown Portland, ME


def geocode_address(address: str, timeout: float = 5.0) -> dict:
    """Return {"lon": float, "lat": float, "matched": bool, "display_name": str|None}.

    "matched" is False when we had to fall back to the default coordinate
    (e.g. no network, no results) so callers can flag lower confidence.
    """
    if not address or not address.strip():
        return {"lon": FALLBACK_LON, "lat": FALLBACK_LAT, "matched": False, "display_name": None}

    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={"q": address, "format": "json", "limit": 1},
            headers={"User-Agent": USER_AGENT},
            timeout=timeout,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            top = results[0]
            return {
                "lon": float(top["lon"]),
                "lat": float(top["lat"]),
                "matched": True,
                "display_name": top.get("display_name"),
            }
    except (requests.RequestException, ValueError, KeyError):
        pass

    return {"lon": FALLBACK_LON, "lat": FALLBACK_LAT, "matched": False, "display_name": None}
