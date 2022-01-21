"""File collection, input, and output."""

import logging
import os
from datetime import datetime
from fnmatch import fnmatch
from glob import glob
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


def copy_files(config):
    """Copy static files."""
    for pattern in config["copy"]:
        filenames = glob(os.path.join(config["src"], pattern))
        filenames = [f for f in filenames if not any(fnmatch(f, p) for p in config["exclude"])]
        filenames = [_pair_src_dst(config, f) for f in filenames]
        for (src_path, dst_path) in filenames:
            _copy_file(src_path, dst_path)


def generate_pages(config, xref, chapters):
    """Generate output for each chapter in turn, filling in cross-references."""
    for info in chapters:
        html = untokenize(config, xref, info["tokens"])
        if "page_template" in config:
            html = _fill_template(config, html)
        _write_file(info["dst"], html)


# ----------------------------------------------------------------------


def _copy_file(src, dst):
    """Copy a file without modification, making directories as needed."""
    LOGGER.debug(f"Copying {dst}.")
    dst = Path(dst)
    dst.parent.mkdir(mode=DIR_PERMS, parents=True, exist_ok=True)
    dst.write_bytes(Path(src).read_bytes())


def _dst_path(config, entry):
    """Construct output path for entry."""
    return os.path.join(config["dst"], entry["slug"], MAIN_DST_FILE)


def _fill_template(config, body):
    """Fill in page template."""
    values = {
        "title": "McCole",
        "content": body,
        "copyrightyear": config["copyrightyear"],
        "author": config["author"],
        "builddate": datetime.today().strftime('%Y-%m-%d')
    }
    return config["page_template"].format(**values)


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


def _pair_src_dst(config, src_file):
    """Construct a pair (src_file, dst_file)."""
    dst_file = os.path.normpath(src_file.replace(config["src"], config["dst"], 1))
    return (src_file, dst_file)


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
