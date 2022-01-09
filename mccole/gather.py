"""Gather data from files."""

def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    overall = {
        "bibkeys": {},
        "order": {}
    }
    for (i, info) in enumerate(files):
        assert info["action"] == "transform"
        assert all(key in info.keys() for key in ["from", "raw", "page"])
        overall["order"][info["from"]] = i + 1
    return overall
