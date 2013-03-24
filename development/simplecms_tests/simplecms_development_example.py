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
# ohne vorher den Pfad angeben zu müssen. Die zwei Zeilen `APPDIR ...` und
# `sys.path.append ...` sind dann nicht mehr notwendig und können entfernt werden.
# ---------
APPDIR = os.path.abspath(os.path.join(THISDIR, "..", ".."))
sys.path.append(APPDIR)
# ---------

import simplecms


# Konfiguriert die "Simple Python CMS"-Instanz und startet den Webserver
simplecms.SimpleCms(
    host = "127.0.0.1",
    port = 8080,
    data_root_dir = os.path.join(THISDIR, "test_instance_data"),
    languages = ["de", "de_AT", "de_DE", "en", "fr"],
    additional_global_config = {
        # Testumgebung aktivieren
        "environment": None,
        "log.screen": True,
        "request.show_tracebacks": True,
        "request.show_mismatched_params": True,
    },
    error_logfile_path = os.path.join(THISDIR, "log", "simplecms_error.log"),
    access_logfile_path = os.path.join(THISDIR, "log", "simplecms_access.log")

    # ToDo: Log-Dateien eintragen



).start()



