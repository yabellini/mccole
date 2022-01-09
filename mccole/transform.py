"""File transformation tools."""

from .util import McColeExc


def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    overall = {
        "order": {}
    }
    for (i, info) in enumerate(files):
        assert info["action"] == "transform"
        assert all(key in info.keys() for key in ["from", "raw", "page"])
        overall["order"][info["from"]] = i + 1
    return overall


def transform_files(config, files):
    """Convert to HTML."""
    for info in files:
        info["cooked"] = info["raw"]
