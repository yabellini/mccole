#!/usr/bin/env python

"""Read, transform, and write."""

import argparse
import logging
from pathlib import Path

from .config import DEFAULTS, get_config
from .files import get_files
from .gather import gather_data
from .transform import transform_files
from .util import McColeExc, fail


def main():
    """Main driver."""
    try:
        options = parse_args()
        _configure_logging(options)
        config = get_config(options.config)

        files = get_files(config, config["src"])
        logging.info(f"found {len(files)} files")
        subset = [info for info in files if info["action"] == "transform"]

        gather_data(config, subset)
        transform_files(config, subset)

        _write_files(config, files)

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
    logging_choices = "debug info warning error critical".split()
    parser.add_argument(
        "--logging",
        type=str,
        choices=logging_choices,
        default="error",
        help="Logging level.",
    )
    return parser.parse_args()


def _configure_logging(options):
    """Set up logging."""
    level_name = options.logging.upper()
    logging.basicConfig(
        level=logging._nameToLevel[level_name], format="%(levelname)s: %(message)s"
    )


def _write_files(config, files):
    """Save all files in a fileset."""
    pass
