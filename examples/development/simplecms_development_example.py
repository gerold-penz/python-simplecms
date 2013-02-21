#!/usr/bin/env python
#coding: utf-8
"""
Simple Python CMS Instanz  - Test- und Entwicklung

Simple Python CMS Instanz konfigurieren und Server starten
"""

import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))

try:
    import simplecms
except ImportError:
    # `sys.path.insert` wird nur zum Testen benötigt.
    # Wenn `simplecms` installiert wurde, kann man es einfach importieren,
    # ohne vorher den Pfad angeben zu müssen.
    sys.path.insert(0, os.path.abspath(os.path.join(THISDIR, "..", "..")))
    import simplecms


# Konfiguriert die "Simple Python CMS"-Instanz und startet den Webserver
simplecms.SimpleCms(
    host = "127.0.0.1",
    port = 8080,
    datadir = os.path.join(THISDIR, "data"),
).start()





