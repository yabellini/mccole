"""Find files."""

import glob
from fnmatch import fnmatch
from pathlib import Path

import frontmatter

from .transform import md_to_doc
from .util import McColeExc


def read_files(config, root):
    """Find files to transform and files to copy."""
    files = []
    for name in glob.glob("**/*", recursive=True):
        p = Path(name)

        # Not a file.
        if not p.is_file():
            continue

        # Ignored.
        if _should_exclude(config, p):
            continue

        # Copied.
        if not _should_transform(config, p):
            files.append({"action": "copy", "from": p, "to": _change_path(config, p)})
            continue

        # Transformed.
        try:
            with open(p, "r") as reader:
                header, raw = frontmatter.parse(reader.read())
                files.append(
                    {
                        "action": "transform",
                        "from": p,
                        "to": _change_path(config, p, ".html"),
                        "header": header,
                        "raw": raw,
                        "doc": md_to_doc(raw),
                    }
                )
        except OSError as exc:
            raise McColeExc(str(exc))

    return files


def write_files(config, files):
    """Save all files in a fileset."""
    pass


def _change_path(config, original, suffix=None):
    """Change source path to destination path."""
    src_base = config["src"].parts
    dst_base = config["dst"].parts
    combined = dst_base + original.parts[len(src_base) :]  # noqa: E203
    # Replace leading double slash with single slash if absolute path.
    result = Path("/".join(combined).replace("//", "/"))
    if suffix is not None:
        result = result.with_suffix("").with_suffix(suffix)
    return result


def _should_exclude(config, p):
    """Ignore this file if it matches an exclusion pattern."""
    return any(fnmatch(p, pat) for pat in config["exclude"])


def _should_transform(config, p):
    """Transform this file if it matches a transformation pattern."""
    return any(fnmatch(p, pat) for pat in config["transform"])
