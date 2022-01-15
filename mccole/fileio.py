"""Read and write files."""

import glob
import logging
from fnmatch import fnmatch
from pathlib import Path

import frontmatter
from mistletoe import Document
from mistletoe.ast_renderer import ASTRenderer

from .config import MAIN_NAME
from .html import md_to_html
from .util import McColeExc


def find_files(config, root):
    """Find files to transform and files to copy."""
    files = []
    for filename in glob.glob(f"{config['src']}/**/*", recursive=True):
        _classify_file(config, files, filename)
    return _reorder_files(config, files)


def write_files(config, xref, files):
    """Save all files in a fileset."""
    for info in files:
        if info["action"] == "copy":
            _copy_file(info["from"], info["to"])
        elif info["action"] == "transform":
            html = md_to_html(config, xref, info["raw"])
            _write_file(info["from"], info["to"], html)
        else:
            raise McColeExc(f"Unknown action {info['action']}")


def md_to_doc(md):
    """Convert Markdown to plain mistletoe Document.

    Need the plain Document in order to find uses of special tags.
    """
    with ASTRenderer() as renderer:  # noqa F841
        return Document(md)


# ----------------------------------------------------------------------


def _change_path(config, original, suffix=None):
    """Change source path to destination path."""
    src_base = Path(config["src"]).parts
    dst_base = Path(config["dst"]).parts
    combined = dst_base + original.parts[len(src_base) :]  # noqa: E203
    # Replace leading double slash with single slash if absolute path.
    result = Path("/".join(combined).replace("//", "/"))
    if suffix is not None:
        result = result.with_suffix("").with_suffix(suffix)
    return result


def _classify_file(config, files, filename):
    """Decide what to do with a file."""
    filepath = Path(filename)

    # Not a file.
    if not filepath.is_file():
        return

    # Ignored.
    if _should_exclude(config, filepath):
        return

    # Copied.
    if not _should_transform(config, filepath):
        files.append(
            {"action": "copy", "from": filepath, "to": _change_path(config, filepath)}
        )
        return

    # Transformed.
    try:
        with open(filepath, "r") as reader:
            header, raw = frontmatter.parse(reader.read())
            files.append(
                {
                    "action": "transform",
                    "from": filepath,
                    "to": _change_path(config, filepath, ".html"),
                    "header": header,
                    "raw": raw,
                    "doc": md_to_doc(raw),
                }
            )
    except OSError as exc:
        raise McColeExc(str(exc))


def _copy_file(from_path, to_path):
    """Copy a file (binary)."""
    logging.debug(f"copying {from_path} to {to_path}")
    try:
        to_path.parent.mkdir(parents=True, exist_ok=True)
        to_path.write_bytes(from_path.read_bytes())
    except IOError as exc:
        raise McColeExc(str(exc))


def _generate_toplevel(config):
    """Generate expected top-level filenames."""
    if "entries" not in config:
        return []
    src = Path(config["src"])
    return [(src / slug / MAIN_NAME) for slug in config["entries"]]


def _reorder_files(config, files):
    """Put chapters and appendices at front and in order."""
    toplevel = set(_generate_toplevel(config))
    front = {}
    back = []
    for info in files:
        if info["from"] in toplevel:
            front[info["from"]] = info
            toplevel.remove(info["from"])
        else:
            back.append(info)
    if toplevel:
        toplevel = ", ".join(sorted(str(toplevel)))
        raise McColeExc(f"Failed to find expected files {toplevel}")
    result = [front[name] for name in _generate_toplevel(config)]
    result.extend(back)
    return result


def _should_exclude(config, p):
    """Ignore this file if it matches an exclusion pattern."""
    return any(fnmatch(p, pat) for pat in config["exclude"])


def _should_transform(config, p):
    """Transform this file if it matches a transformation pattern."""
    return any(fnmatch(p, pat) for pat in config["transform"])


def _write_file(from_path, to_path, text):
    """Write a file."""
    logging.debug(f"transforming {from_path} to {to_path}")
    try:
        to_path.parent.mkdir(parents=True, exist_ok=True)
        to_path.write_text(text)
    except IOError as exc:
        raise McColeExc(str(exc))
