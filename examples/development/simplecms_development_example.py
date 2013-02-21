# coding: utf-8

import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))

try:
    import simplecms
except ImportError:
    # SIMPLECMSDIR und `sys.path.insert` werden nur zum Testen benötigt.
    # Wenn `simplecms` installiert wurde, kann man es einfach importieren,
    # ohne vorher den Pfad angeben zu müssen.
    SIMPLECMSDIR = os.path.abspath(os.path.join(THISDIR, "..", ".."))
    sys.path.insert(0, SIMPLECMSDIR)
    import simplecms

DATADIR = os.path.join(THISDIR, "data")


def main():

    pass

if __name__ == "__main__":
    main()

