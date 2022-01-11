"""Scraps for future use."""

from collections.abc import Sequence
from types import SimpleNamespace


def json_to_ns(obj, root=False):
    """Recursively convert JSON-compatible structure to namespace."""
    if (obj is None) and root:
        return {}
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, Sequence):
        return list(obj)
    elif isinstance(obj, dict):
        return SimpleNamespace(**{k: json_to_ns(v) for (k, v) in obj.items()})
    else:
        return obj
