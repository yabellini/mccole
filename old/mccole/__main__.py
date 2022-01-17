"""Make McCole module runnable."""

import sys

from .mccole import mccole
from .util import McColeExc

if __name__ == "__main__":
    try:
        mccole(sys.argv[1:])
    except McColeExc as exc:
        print(exc.msg, file=sys.stderr)
        sys.exit(1)
