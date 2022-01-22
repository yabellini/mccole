"""Run simple server for previewing."""

import http.server
import logging
import socketserver

from .util import LOGGER_NAME


LOGGER = logging.getLogger(LOGGER_NAME)


class server(socketserver.TCPServer):
    allow_reuse_address = True


def run_server(options, root_dir):
    """Run web server on specified port."""
    if not options.run:
        return

    class handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=root_dir, **kwargs)

    with server(("", options.run), handler) as httpd:
        LOGGER.info(f"serving port {options.run}")
        httpd.serve_forever()
