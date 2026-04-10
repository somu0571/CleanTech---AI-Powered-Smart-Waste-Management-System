"""
routing.py – AI Route Optimisation Engine
Algorithm : Nearest-Neighbour Greedy VRP (Vehicle Routing Problem)
Input     : Hotspot data from forecasting module
Output    : Ordered stops, distance saved, fuel & carbon savings
"""

import math
import random
from typing import List, Tuple


# ── Types ─────────────────────────────────────────────────────────────────────

Point = Tuple[float, float]   # (lat, lon)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _haversine(a: Point, b: Point) -> float:
    """Returns distance in kilometres between two lat/lon points."""
    R = 6371.0
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def _route_distance(route: List[Point]) -> float:
    total = 0.0
    for i in range(len(route) - 1):
        total += _haversine(route[i], route[i + 1])
    return round(total, 3)


def _nearest_neighbour(depot: Point, stops: List[dict]) -> List[dict]:
    """Greedy nearest-neighbour TSP solver."""
    remaining  = stops[:]
    route      = []
    current    = depot

    while remaining:
        nearest  = min(remaining,
                       key=lambda s: _haversine(current, (s["lat"], s["lon"])))
        route.append(nearest)
        current  = (nearest["lat"], nearest["lon"])
        remaining.remove(nearest)

    return route


# ── Public API ────────────────────────────────────────────────────────────────

def get_optimised_route(hotspots: List[dict]) -> dict:
    """
    hotspots: [{"zone": str, "lat": float, "lon": float, "waste_kg": float}]

    Returns:
        {
            "route":          [ordered hotspot dicts],
            "total_km":       float,
            "saved_km":       float,
            "fuel_saved_L":   float,
            "carbon_saved_kg":float,
            "stops":          int,
        }
    """
    if not hotspots:
        # Generate demo hotspots
        hotspots = _demo_hotspots()

    depot   = (19.07, 72.87)   # Municipal depot (Mumbai)
    ordered = _nearest_neighbour(depot, hotspots)

    # Optimised distance
    opt_coords = [depot] + [(s["lat"], s["lon"]) for s in ordered] + [depot]
    opt_km     = _route_distance(opt_coords)

    # Naïve distance (original order)
    naive_coords = [depot] + [(s["lat"], s["lon"]) for s in hotspots] + [depot]
    naive_km     = _route_distance(naive_coords)

    saved_km = round(max(naive_km - opt_km, 0), 3)

    # Simulated fuel & carbon (diesel truck: ~0.35 L/km, CO₂: 2.68 kg/L)
    fuel_saved    = round(saved_km * 0.35, 2)
    carbon_saved  = round(fuel_saved * 2.68, 2)

    return {
        "route":           ordered,
        "total_km":        opt_km,
        "naive_km":        naive_km,
        "saved_km":        saved_km,
        "fuel_saved_L":    fuel_saved,
        "carbon_saved_kg": carbon_saved,
        "stops":           len(ordered),
        "depot":           {"lat": depot[0], "lon": depot[1], "zone": "Depot"},
    }


def _demo_hotspots() -> List[dict]:
    """Fallback demo hotspots around Mumbai."""
    spots = [
        ("Zone A – North",   19.22, 72.85, 95.3),
        ("Zone B – East",    19.08, 72.92, 76.1),
        ("Zone C – South",   18.92, 72.83, 112.8),
        ("Zone D – West",    19.10, 72.78, 58.4),
        ("Zone E – Central", 19.07, 72.87, 88.0),
    ]
    return [{"zone": z, "lat": lat + random.uniform(-0.005, 0.005),
             "lon": lon + random.uniform(-0.005, 0.005), "waste_kg": w}
            for z, lat, lon, w in spots]