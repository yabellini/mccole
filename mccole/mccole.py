"""Main entry point."""

import argparse
import http.server
import logging
import os
import socketserver
import sys

from .bib import load_bib
from .config import DEFAULT_CONFIG_FILE, DEFAULTS, get_config
from .crossref import cross_reference
from .fileio import collect_chapters, copy_files, generate_pages
from .gloss import load_gloss
from .translate import tokenize
from .util import LOGGER_NAME, McColeExc, pretty

# ----------------------------------------------------------------------


LOGGING_LEVELS = "debug info warning error critical".split()
LOGGER = None


def main(args):
    """Parse arguments and execute."""
    try:
        options = _parse_args(args)
        _setup(options)
        config = get_config(options.config)
        LOGGER.info(f"configuration is {pretty(config)}")

        load_bib(config)
        load_gloss(config)
        _load_template(config)

        chapters = collect_chapters(config)
        LOGGER.info(f"chapters are {pretty(chapters)}")

        tokenize(config, chapters)
        xref = cross_reference(config, chapters)
        LOGGER.info(f"xref is {pretty(xref)}")

        generate_pages(config, xref, chapters)
        copy_files(config)

        _run_server(options, config["dst"])

    except McColeExc as exc:
        LOGGER.error(f"McCole failed: {exc.msg}")
        sys.exit(1)


# ----------------------------------------------------------------------


def _load_template(config):
    """Load page template."""
    if "template" not in config:
        config["page_template"] = None
    else:
        with open(config["template"], "r") as reader:
            config["page_template"] = reader.read()


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
    parser.add_argument("-r", "--run", type=int, help="Run server on specified port.")
    parser.add_argument(
        "-s", "--src", type=str, default=DEFAULTS["src"], help="Source directory."
    )
    return parser.parse_args(args)


def _run_server(options, root_dir):
    """Run web server on specified port."""
    if not options.run:
        return

    class handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root_dir, **kwargs)

    with socketserver.TCPServer(("", options.run), handler) as httpd:
        try:
            LOGGER.info(f"serving port {options.run}")
            httpd.serve_forever()
        finally:
            httpd.server_close()


def _setup(options):
    """Do initial setup."""
    # Logging.
    global LOGGER
    level_name = options.logging.upper()
    logging.basicConfig(format="%(levelname)s: %(message)s")
    LOGGER = logging.getLogger(LOGGER_NAME)
    LOGGER.setLevel(logging._nameToLevel[level_name])

    # Working directory.
    if options.chdir is not None:
        logging.info(f"changing working directory to {options.chdir}")
        os.chdir(options.chdir)
