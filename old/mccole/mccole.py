"""Read, transform, and write."""

import argparse
import logging
import os
from pathlib import Path

from .config import DEFAULT_CONFIG_PATH, DEFAULTS, get_config
from .fileio import find_files, write_files
from .gather import gather_data

LOGGING_CHOICES = "debug info warning error critical".split()


def mccole(args):
    """Main driver."""
    options = _parse_args(args)
    _setup(options)

    config = get_config(options.config)
    logging.debug(f"config is {config}")

    files = find_files(config, config["src"])
    logging.info(f"found {len(files)} files")

    xref = gather_data(config, files)
    logging.debug(f"xref with gathered data is {xref}")

    write_files(config, xref, files)


def _parse_args(args):
    """Get command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-d", "--dst", type=Path, default=DEFAULTS["dst"], help="Destination directory."
    )
    parser.add_argument(
        "-C",
        "--chdir",
        type=Path,
        default=None,
        help="Change directory before running.",
    )
    parser.add_argument(
        "-g",
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Configuration file.",
    )
    parser.add_argument(
        "-L",
        "--logging",
        type=str,
        choices=LOGGING_CHOICES,
        default="error",
        help="Logging level.",
    )
    parser.add_argument(
        "-s", "--src", type=Path, default=DEFAULTS["src"], help="Source directory."
    )
    return parser.parse_args(args)


def _setup(options):
    """Do initial setup."""
    # Logging.
    level_name = options.logging.upper()
    logging.basicConfig(
        level=logging._nameToLevel[level_name], format="%(levelname)s: %(message)s"
    )

    # Working directory.
    if options.chdir is not None:
        logging.info(f"changing working directory to {options.chdir}")
        os.chdir(options.chdir)
