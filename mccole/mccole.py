"""Read, transform, and write."""

import argparse
import logging
import os
from pathlib import Path

from .config import DEFAULT_CONFIG_PATH, DEFAULTS, get_config
from .evaluate import create_env
from .fileio import read_files, write_files
from .gather import gather_data
from .html import md_to_html
from .latex import md_to_latex


LOGGING_CHOICES = "debug info warning error critical".split()
CONVERTERS = {
    'html': md_to_html,
    'latex': md_to_latex
}
FORMAT_CHOICES = CONVERTERS.keys()


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

    config = gather_data(config, files)
    logging.debug(f"config with gathered data is {config}")

    _create_output(config, files, CONVERTERS[options.format])
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
        "-f",
        "--format",
        choices=FORMAT_CHOICES,
        default="html",
        help="Output format.",
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


def _configure_logging(options):
    """Set up logging."""
    level_name = options.logging.upper()
    logging.basicConfig(
        level=logging._nameToLevel[level_name], format="%(levelname)s: %(message)s"
    )

def _create_output(config, files, converter):
    """Create output file content."""
    for info in files:
        if info["action"] == "transform":
            info["html"] = converter(info["raw"], config)
