"""Read inputs."""

import os

from .config import MAIN_DST_FILE, MAIN_SRC_FILE


def collect_pages(config):
    """Return page information."""
    major = 0
    result = []
    for entry in config["chapters"]:
        major = _next_major(entry, major)
        result.append({
            "slug": entry["slug"],
            "src": _src_path(config, entry),
            "dst": _dst_path(config, entry),
            "major": major,
            "tokens": None,
        })

    if "root" in config:
        result.append({
            "slug": "_index",
            "src": os.path.join(config["src"], config["root"]),
            "dst": os.path.join(config["dst"], "index.html"),
            "major": None,
            "tokens": None
        })

    return result


# ----------------------------------------------------------------------


def _dst_path(config, entry):
    """Construct output path for entry."""
    return os.path.join(config["dst"], entry["slug"], MAIN_DST_FILE)


def _next_major(entry, major):
    """Create next major heading index."""
    # First appendix.
    if entry.get("appendix", False):
        return "A"

    # Chapters are numbered.
    if isinstance(major, int):
        return major + 1

    # Appendices are lettered.
    assert isinstance(major, str) and (len(major) == 1)
    return chr(ord(major) + 1)


def _src_path(config, entry):
    """Construct input path for entry."""
    # Explicit source file (e.g., "LICENSE.md" => "license/index.md").
    if "file" in entry:
        return os.path.join(config["src"], entry["file"])

    # Default source file.
    return os.path.join(config["src"], entry["slug"], MAIN_SRC_FILE)
