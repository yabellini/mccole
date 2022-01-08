"""Find files."""

import glob
from fnmatch import fnmatch
from pathlib import Path


def find_files(config, root):
    """Find files to transform and files to copy."""
    files = []
    for name in glob.glob("**/*", recursive=True):
        p = Path(name)
        if not p.is_file():
            continue
        elif _should_exclude(config, p):
            continue
        elif _should_transform(config, p):
            files.append({
                "action": "transform",
                "from": p,
                "to": _change_path(config, p, ".html")
            })
        else:
            files.append({
                "action": "copy",
                "from": p,
                "to": _change_path(config, p)
            })
    return files


def _change_path(config, original, suffix=None):
    """Change source path to destination path."""
    src_base = config["src"].parts
    dst_base = config["dst"].parts
    combined = dst_base + original.parts[len(src_base) :]
    # Replace leading double slash with single slash if absolute path.
    result = Path("/".join(combined).replace("//", "/"))
    if suffix is not None:
        result = result.with_suffix("").with_suffix(suffix)
    return result


def _should_exclude(config, p):
    return any(fnmatch(p, pat) for pat in config["exclude"])


def _should_transform(config, p):
    return any(fnmatch(p, pat) for pat in config["transform"])
