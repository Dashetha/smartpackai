# backend/utils/helpers.py
import math
from typing import Tuple

def calculate_volume(dimensions: Tuple[float, float, float]) -> float:
    """Calculate volume from dimensions (L, W, H)"""
    return math.prod(dimensions)

def calculate_volumetric_weight(dimensions: Tuple[float, float, float], factor: float = 5000) -> float:
    """
    Calculate volumetric weight (dimensions in cm)
    Formula: (L × W × H) / factor
    Common factors: 5000 (metric), 139 (imperial)
    """
    return calculate_volume(dimensions) / factor

def calculate_savings(current_volume: float, optimized_volume: float, rate: float = 0.01) -> float:
    """
    Calculate cost savings from volume reduction
    rate: cost per cm³ in USD
    """
    return (current_volume - optimized_volume) * rate

def convert_units(value: float, from_unit: str, to_unit: str) -> float:
    """Convert between measurement units"""
    conversions = {
        'cm_to_in': 0.393701,
        'in_to_cm': 2.54,
        'kg_to_lb': 2.20462,
        'lb_to_kg': 0.453592
    }
    key = f"{from_unit}_to_{to_unit}"
    if key in conversions:
        return value * conversions[key]
    raise ValueError(f"Unsupported conversion: {from_unit} to {to_unit}")