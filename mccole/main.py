#!/usr/bin/env python

"""Read, transform, and write."""

import argparse
from pathlib import Path
import yaml

from mccole.files import find_files
from mccole.transform import gather_data, parse_files, transform_files
from mccole.util import DEFAULTS, McColeExc, fail, obj2ns


def main():
    """Main driver."""
    try:
        options = parse_args()
        config = get_config(options.config)
        to_transform, to_copy = find_files(config, config.src)
        parse_files(config, to_transform)
        gather_data(config, to_transform)
        transform_files(config, to_transform)
        write_files(config, to_transform)
        copy_files(config, to_copy)
    except McColeExc as exc:
        fail(exc)


def parse_args():
    """Get command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--dst", type=Path, default=DEFAULTS.dst, help="Destination directory."
    )
    parser.add_argument(
        "--config", type=Path, default=DEFAULTS.config, help="Configuration file."
    )
    parser.add_argument(
        "--src", type=Path, default=DEFAULTS.src, help="Source directory."
    )
    return parser.parse_args()


def get_config(filename):
    """Load configuration file."""
    try:
        with open(filename, "r") as reader:
            loaded = yaml.safe_load(reader)
            return obj2ns(loaded, root=True)
    except OSError as exc:
        raise McColeExc(str(exc))


def write_files(config, files):
    """Save all files in a fileset."""
    pass


def copy_files(config, files):
    """Copy all files in a fileset."""
    pass


if __name__ == "__main__":
    main()
