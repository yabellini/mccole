"""Make McCole module runnable."""

import sys

from .mccole import main
from .util import McColeExc

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except McColeExc as exc:
        print(exc.msg, file=sys.stderr)
        sys.exit(1)
