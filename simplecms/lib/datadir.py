#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import config


def init(datadir):
    """
    Initialisiert den Datenordner
    """

    # Datenordner-Konfiguration setzen
    config.DATADIR.value = datadir

    # Benötigte Ordner erstellen
    create_dirs()


def create_dirs():
    """
    Erstellt den Datenordner und die benötigten Unterordner,
    falls diese noch nicht existieren.
    """

    # Hauptordner
    datadir = config.DATADIR.value
    assert datadir
    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    # JavaScript-Ordner
    datajsdir = config.DATAJSDIR.value
    if not os.path.isdir(datajsdir):
        os.makedirs(datajsdir)

    # CSS-Ordner
    datacssdir = config.DATACSSDIR.value
    if not os.path.isdir(datacssdir):
        os.makedirs(datacssdir)

    # Datenbaum-Ordner
    datatreedir = config.DATATREEDIR.value
    if not os.path.isdir(datatreedir):
        os.makedirs(datatreedir)
