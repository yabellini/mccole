"""Find files."""

import glob
from fnmatch import fnmatch
from pathlib import Path


def find_files(config, root):
    """Find files to transform and files to copy."""
    transform, copy = {}, {}
    for name in glob.glob("**/*", recursive=True):
        p = Path(name)
        if not p.is_file():
            continue
        elif _should_exclude(config, p):
            continue
        elif _should_transform(config, p):
            transform[p] = {}
        else:
            copy[p] = {}
    return transform, copy


def _should_exclude(config, p):
    return any(fnmatch(p, pat) for pat in config["exclude"])


def _should_transform(config, p):
    return any(fnmatch(p, pat) for pat in config["transform"])
