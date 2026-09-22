"""Small, explainable Shannon entropy implementation."""
import math
from collections import Counter

def shannon_entropy(data: bytes) -> float:
    """Return Shannon entropy in bits per byte, from 0 to 8."""
    if not data:
        return 0.0
    total = len(data)
    return -sum((count / total) * math.log2(count / total) for count in Counter(data).values())

def entropy_label(value: float) -> str:
    """Classify entropy for a human-readable forensic report."""
    if value >= 7.5: return 'very-high'
    if value >= 6.0: return 'high'
    if value >= 3.0: return 'medium'
    return 'low'
