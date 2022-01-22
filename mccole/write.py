"""Write outputs."""

import logging
import os
from datetime import datetime
from fnmatch import fnmatch
from glob import glob
from pathlib import Path

from .render import render
from .util import LOGGER_NAME, err, obj_to_namespace

# Directory permissions.
DIR_PERMS = 0o755

# Character encoding.
ENCODING = "utf-8"

# Where to report.
LOGGER = logging.getLogger(LOGGER_NAME)


# ----------------------------------------------------------------------


def copy_files(config):
    """Copy static files."""
    for pattern in config["copy"]:
        filenames = glob(os.path.join(config["src"], pattern))
        filenames = [
            f for f in filenames if not any(fnmatch(f, p) for p in config["exclude"])
        ]
        filenames = [_pair_src_dst(config, f) for f in filenames]
        for (src_path, dst_path) in filenames:
            _copy_file(src_path, dst_path)


def generate_pages(config, xref):
    """Generate output for each chapter in turn, filling in cross-references."""
    seen = {
        "cite": set(),
        "figure_ref": set(),
        "gloss_ref": set(),
        "index_ref": set(),
        "table_ref": set(),
    }
    site = obj_to_namespace(
        {
            "title": "McCole",
            "copyrightyear": config["copyrightyear"],
            "author": config["author"],
            "builddate": datetime.today().strftime("%Y-%m-%d"),
        }
    )
    for info in config["pages"]:
        html = render(config, xref, seen, info)
        page = obj_to_namespace({"content": html})
        html = _fill_template(config, info, site, page)
        _write_file(info["dst"], html)
    return seen


# ----------------------------------------------------------------------


def _copy_file(src, dst):
    """Copy a file without modification, making directories as needed."""
    LOGGER.debug(f"Copying {dst}.")
    dst = Path(dst)
    dst.parent.mkdir(mode=DIR_PERMS, parents=True, exist_ok=True)
    dst.write_bytes(Path(src).read_bytes())


def _fill_template(config, info, site, page):
    """Fill in page template if present."""
    template_name = info["metadata"].get("template", None)
    if not template_name:
        return page.content

    template = config["template"].get(template_name, None)
    if not template:
        err(config, f"Unknown template {template_name} in {info['src']}.")
        return page.content

    return template.format(site=site, page=page)


def _pair_src_dst(config, src_file):
    """Construct a pair (src_file, dst_file)."""
    dst_file = os.path.normpath(src_file.replace(config["src"], config["dst"], 1))
    return (src_file, dst_file)


def _write_file(dst, html):
    """Write a file, making directories if needed."""
    LOGGER.debug(f"Writing {dst}.")
    dst = Path(dst)
    dst.parent.mkdir(mode=DIR_PERMS, parents=True, exist_ok=True)
    dst.write_text(html, encoding=ENCODING)
