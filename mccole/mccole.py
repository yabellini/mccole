"""Read, transform, and write."""

import argparse
import logging
import os
import sys
from pathlib import Path

from .config import DEFAULTS, get_config
from .evaluate import create_env
from .fileio import read_files, write_files
from .gather import gather_data
from .util import McColeExc


def mccole(args):
    """Main driver."""
    options = _parse_args(args)
    if options.chdir is not None:
        os.chdir(options.chdir)
    _configure_logging(options)

    config = get_config(options.config)

    files = read_files(config, config["src"])
    logging.info(f"found {len(files)} files")

    subset = [info for info in files if info["action"] == "transform"]
    gather_data(config, subset)

    create_env(config)
    write_files(config, files)


def _parse_args(args):
    """Get command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-d", "--dst", type=Path, default=DEFAULTS["dst"], help="Destination directory."
    )
    parser.add_argument(
        "-C", "--chdir", type=Path, default=None, help="Change directory before running."
    )
    parser.add_argument(
        "-F", "--config", type=Path, default=DEFAULTS["config"], help="Configuration file."
    )
    parser.add_argument(
        "-s", "--src", type=Path, default=DEFAULTS["src"], help="Source directory."
    )
    logging_choices = "debug info warning error critical".split()
    parser.add_argument(
        "-L",
        "--logging",
        type=str,
        choices=logging_choices,
        default="error",
        help="Logging level.",
    )
    return parser.parse_args(args)


def _configure_logging(options):
    """Set up logging."""
    level_name = options.logging.upper()
    logging.basicConfig(
        level=logging._nameToLevel[level_name], format="%(levelname)s: %(message)s"
    )
