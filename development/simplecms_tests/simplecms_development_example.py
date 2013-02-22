#!/usr/bin/env python
#coding: utf-8
"""
Simple Python CMS Instanz  - Test- und Entwicklung

Simple Python CMS Instanz konfigurieren und Server starten
"""

import os
import sys

THISDIR = os.path.dirname(os.path.abspath(__file__))

# Nachdem `simplecms` installiert wurde, kann man es einfach importieren,
# ohne vorher den Pfad angeben zu müssen.
# ---------
APPDIR = os.path.abspath(os.path.join(THISDIR, "..", ".."))
sys.path.append(APPDIR)
# ---------

import simplecms


# Konfiguriert die "Simple Python CMS"-Instanz und startet den Webserver
simplecms.SimpleCms(
    host = "127.0.0.1",
    port = 8080,
    datadir = os.path.join(THISDIR, "test_instance_data"),
    additional_global_config = {
        # Testumgebung aktivieren
        "environment": None,
        "log.screen": True,
        "request.show_tracebacks": True,
        "request.show_mismatched_params": True,
    }
).start()



