"""Find files."""

import glob
from fnmatch import fnmatch
from pathlib import Path

import frontmatter
from mistletoe import Document
from mistletoe.ast_renderer import ASTRenderer

from .util import McColeExc


def get_files(config, root):
    """Find files to transform and files to copy."""
    files = []
    for name in glob.glob("**/*", recursive=True):
        p = Path(name)

        if not p.is_file():
            continue

        if _should_exclude(config, p):
            continue

        if not _should_transform(config, p):
            files.append({"action": "copy", "from": p, "to": _change_path(config, p)})
            continue

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
                        "doc": md_to_doc(raw)
                    }
                )
        except OSError as exc:
            raise McColeExc(str(exc))

    return files


def md_to_doc(md):
    """Convert Markdown to mistletoe Document."""
    with ASTRenderer() as renderer:
        return Document(md)


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
    return any(fnmatch(p, pat) for pat in config["exclude"])


def _should_transform(config, p):
    return any(fnmatch(p, pat) for pat in config["transform"])
