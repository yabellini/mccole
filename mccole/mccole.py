"""Main entry point."""

import argparse
import logging
import os
import sys

from .bib import load_bib
from .gloss import load_gloss
from .collect import collect_chapters
from .config import DEFAULT_CONFIG_FILE, DEFAULTS, get_config
from .crossref import cross_reference
from .generate import generate
from .translate import tokenize
from .util import LOGGER_NAME, McColeExc, pretty

# ----------------------------------------------------------------------


LOGGING_LEVELS = "debug info warning error critical".split()


def main(args):
    """Parse arguments and execute."""
    try:
        options = _parse_args(args)
        logger = _setup(options)
        config = get_config(options.config)
        logger.info(f"configuration is {pretty(config)}")

        load_bib(config)
        load_gloss(config)

        chapters = collect_chapters(config)
        logger.info(f"chapters are {pretty(chapters)}")

        tokenize(config, chapters)
        xref = cross_reference(config, chapters)
        logger.info(f"xref is {pretty(xref)}")

        generate(config, xref, chapters)

    except McColeExc as exc:
        logger.error(f"McCole failed: {exc.msg}")
        sys.exit(1)


# ----------------------------------------------------------------------


def _parse_args(args):
    """Handle command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-d", "--dst", type=str, default=DEFAULTS["dst"], help="Destination directory."
    )
    parser.add_argument(
        "-C",
        "--chdir",
        type=str,
        default=None,
        help="Change directory before running.",
    )
    parser.add_argument(
        "-g",
        "--config",
        type=str,
        default=DEFAULT_CONFIG_FILE,
        help="Configuration file.",
    )
    parser.add_argument(
        "-L",
        "--logging",
        type=str,
        choices=LOGGING_LEVELS,
        default="error",
        help="Logging level.",
    )
    parser.add_argument(
        "-s", "--src", type=str, default=DEFAULTS["src"], help="Source directory."
    )
    return parser.parse_args(args)


def _setup(options):
    """Do initial setup."""
    # Logging.
    level_name = options.logging.upper()
    logging.basicConfig(format="%(levelname)s: %(message)s")
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging._nameToLevel[level_name])

    # Working directory.
    if options.chdir is not None:
        logging.info(f"changing working directory to {options.chdir}")
        os.chdir(options.chdir)

    return logger
