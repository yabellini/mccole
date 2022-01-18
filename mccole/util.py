"""Utilities."""


# Identify this module's logger.
LOGGER_NAME = "mccole"


class McColeExc(Exception):
    """Problems we expect."""

    def __init__(self, msg):
        """Save the message."""
        self.msg = msg
