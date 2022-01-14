"""Read, transform, and write."""

import argparse
import logging
import os
from pathlib import Path

from .config import DEFAULT_CONFIG_PATH, DEFAULTS, get_config
from .convert import create_output
from .fileio import read_files, write_files
from .gather import gather_data
from .html import doc_to_html


def mccole(args):
    """Main driver."""
    options = _parse_args(args)
    _configure_logging(options)
    if options.chdir is not None:
        logging.info(f"changing working directory to {options.chdir}")
        os.chdir(options.chdir)

    config = get_config(options.config)
    logging.debug(f"config is {config}")

    files = read_files(config, config["src"])
    logging.info(f"found {len(files)} files")
    logging.debug(", ".join([str(info["from"]) for info in files]))

    gather_data(config, files)
    logging.debug(f"config with gathered data is {config}")

    create_output(config, files, doc_to_html)
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
        "-C",
        "--chdir",
        type=Path,
        default=None,
        help="Change directory before running.",
    )
    parser.add_argument(
        "-F",
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH,
        help="Configuration file.",
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
