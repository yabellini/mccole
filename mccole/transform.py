"""File transformation tools."""


def transform_files(config, files):
    """Convert to HTML."""
    for info in files:
        info["cooked"] = info["raw"]
