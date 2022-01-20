"""File collection, input, and output."""

import logging
import os
from pathlib import Path

from .config import MAIN_DST_FILE, MAIN_SRC_FILE
from .translate import untokenize
from .util import LOGGER_NAME

# Directory permissions.
DIR_PERMS = 0o755

# Character encoding.
ENCODING = "utf-8"

# Where to report.
LOGGER = logging.getLogger(LOGGER_NAME)


# ----------------------------------------------------------------------


def collect_chapters(config):
    """Return chapter files."""
    major = 0
    result = []
    for entry in config["chapters"]:
        major = _next_major(entry, major)
        result.append(
            {
                "slug": entry["slug"],
                "src": _src_path(config, entry),
                "dst": _dst_path(config, entry),
                "major": major,
                "tokens": None,
            }
        )
    return result


def generate(config, xref, chapters):
    """Generate output for each chapter in turn, filling in cross-references."""
    for info in chapters:
        html = untokenize(config, xref, info["tokens"])
        _write_file(info["dst"], html)


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


def _write_file(dst, html):
    """Write a file, making directories if needed."""
    LOGGER.debug(f"Writing {dst}.")
    dst = Path(dst)
    dst.parent.mkdir(mode=DIR_PERMS, parents=True, exist_ok=True)
    dst.write_text(html, encoding=ENCODING)
