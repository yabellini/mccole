#!/usr/bin/env python

"""Read, transform, and write."""

import argparse
from pathlib import Path

from .config import DEFAULTS, get_config
from .files import find_files
from .transform import gather_data, parse_files, transform_files
from .util import McColeExc, fail


def main():
    """Main driver."""
    try:
        options = parse_args()
        config = get_config(options.config)
        files = find_files(config, config["src"])
        if options.verbose:
            print(f"found {len(files)} files")
        subset = [info for info in files if info["action"] == "transform"]
        parse_files(config, subset)
        gather_data(config, subset)
        transform_files(config, subset)
        write_files(config, files)
    except McColeExc as exc:
        fail(exc)


def parse_args():
    """Get command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--dst", type=Path, default=DEFAULTS["dst"], help="Destination directory."
    )
    parser.add_argument(
        "--config", type=Path, default=DEFAULTS["config"], help="Configuration file."
    )
    parser.add_argument(
        "--src", type=Path, default=DEFAULTS["src"], help="Source directory."
    )
    parser.add_argument("--verbose", action="store_true", help="Report progress.")
    return parser.parse_args()


def write_files(config, files):
    """Save all files in a fileset."""
    pass


def copy_files(config, files):
    """Copy all files in a fileset."""
    pass
