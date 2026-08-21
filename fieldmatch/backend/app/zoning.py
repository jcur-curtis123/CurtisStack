"""
Duplex / multi-unit eligibility logic.

Grounded in Maine's LD 2003 (PL 2021, ch. 672, "An Act to Implement the
Recommendations of the Commission to Increase Housing Opportunities in
Maine by Studying Zoning and Land Use Restrictions"), as amended by LD 1706.

Key provisions this encodes:
  - Statewide, municipalities must allow at least 2 residential units on
    any lot where a single-family home is (or would be) allowed by right.
  - Within a municipality's "designated growth area," that floor rises to
    up to 4 units.
  - Municipalities cannot use minimum lot size, parking minimums, or
    similar dimensional standards to functionally defeat the 2-unit
    allowance, though other dimensional/setback/septic rules still apply.
  - Shoreland zones (regulated separately under Maine's Mandatory
    Shoreland Zoning Act) and zones that don't allow residential use at
    all (heavy industrial, resource protection) are treated as carve-outs
    that need case-by-case review rather than an automatic yes.

This is a simplified, general-purpose model for demo/reference use — it
is NOT a substitute for a municipality's actual zoning ordinance or a
call to the local code enforcement / planning office. Real answers can
turn on overlay districts, historic-district rules, septic capacity,
flood zones, and ordinance amendments made after this was written.
"""

from typing import Optional


# Zones where residential use isn't permitted at all, so LD 2003's
# 2-unit floor doesn't attach (no "as of right" single-family baseline
# to build from).
NON_RESIDENTIAL_ZONES = {"I-L", "I-M", "I-H", "IND"}

# Zones explicitly for open space / conservation — development is
# restricted independent of the housing-density statute.
CONSERVATION_ZONES = {"POS", "RP", "CONS"}


def assess_duplex_eligibility(
    zone: Optional[str],
    lot_area_sqft: Optional[float],
    growth_area: bool = False,
    shoreland: bool = False,
) -> dict:
    """Return a structured eligibility assessment for adding a second
    (or up to fourth) dwelling unit on a parcel, given its zone and a
    few overlay flags.
    """
    zone = (zone or "").upper().strip()

    if not zone:
        return {
            "eligible": None,
            "max_units": None,
            "basis": "No zoning classification available for this parcel.",
            "caveats": ["Zone code missing from parcel data."],
            "confidence": 0.2,
        }

    if zone in CONSERVATION_ZONES:
        return {
            "eligible": False,
            "max_units": 1,
            "basis": (
                f"{zone} is a conservation/open-space designation. LD 2003's "
                "density floor applies to zones with an existing single-family "
                "residential allowance, which this zone does not have."
            ),
            "caveats": ["Confirm with the planning office before ruling this out entirely."],
            "confidence": 0.75,
        }

    if zone in NON_RESIDENTIAL_ZONES:
        return {
            "eligible": False,
            "max_units": 0,
            "basis": (
                f"{zone} is a non-residential (industrial) zone. Residential use "
                "isn't permitted by right, so LD 2003's 2-unit floor doesn't apply here. "
                "A rezoning or variance would be required."
            ),
            "caveats": ["Mixed-use overlays occasionally allow residential in industrial zones — worth checking."],
            "confidence": 0.7,
        }

    # Everything else is treated as a residential (or residential-permitting)
    # zone, which is the case LD 2003 targets directly.
    max_units = 4 if growth_area else 2
    caveats = [
        "Local dimensional standards (setbacks, height, lot coverage, septic/water capacity) "
        "still apply and can constrain what actually fits on the lot.",
        "This is a general reference based on LD 2003, not a review of the municipality's "
        "adopted ordinance — confirm with the local planning/code enforcement office before acting.",
    ]

    if shoreland:
        caveats.insert(
            0,
            "This parcel falls in a Shoreland Zoning overlay, which is regulated separately "
            "under state shoreland law and can further restrict density regardless of the "
            "underlying zone.",
        )
        confidence = 0.55
    else:
        confidence = 0.8

    if lot_area_sqft is not None and lot_area_sqft < 3000:
        caveats.insert(
            0,
            "The lot is quite small (under 3,000 sq ft). LD 2003 protects the legal right to "
            "add a unit, but septic capacity, setbacks, or lot coverage may still make it hard "
            "to physically fit a second structure or addition.",
        )

    basis = (
        f"{zone} permits single-family residential use, so under LD 2003 the lot must be "
        f"allowed at least 2 dwelling units by right"
        + (f", rising to up to {max_units} because it falls within the municipality's designated growth area" if growth_area else "")
        + "."
    )

    return {
        "eligible": True,
        "max_units": max_units,
        "basis": basis,
        "caveats": caveats,
        "confidence": confidence,
    }
