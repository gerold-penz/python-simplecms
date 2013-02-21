#!/usr/bin/env python
# coding: utf-8
"""
Grundkonfigurationen des Programmes lesen und initialisieren

Die Grundkonfiguration ist in `cherrypy.config` gespeichert.
Die Grundeinstellungen werden beim Start der Anwendung eingestellt und dürfen
im laufenden Betrieb nicht mehr verändert werden.

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import cherrypy


# Dictionary mit allen Einstellungen
all_configurations = {}


class Config(object):
    """
    Repräsentiert eine Konfiguration
    """

    locked = True


    def __init__(
        self,
        name,
        short_description,
        long_description = None,
        default = None
    ):

        self.name = unicode(name)
        self.short_description = unicode(short_description)
        self.long_description = unicode(long_description) if long_description else None
        self.default = default

        # Einstellung in das globale Dict legen
        all_configurations[name] = self


    def __str__(self):
        """
        Gibt die UTF-8 Repräsentation des Konfigurationsnamens zurück
        """

        return self.name.encode("utf-8")


    def __unicode__(self):
        """
        Gibt die Unicode-Repräsentation des Konfigurationsnamens zurück
        """

        return unicode(self.name)


    def get(self):
        """
        Gibt den Wert der Einstellung zurück
        """

        return cherrypy.config.get(self.name, self.default)


    def set(self, value):
        """
        Schreibt die Konfiguration nach *cherrypy.config*
        """

        if self.locked:
            raise RuntimeError("Changing %s is not allowed" % self.name)
        cherrypy.config[self.name] = value


    value = property(get, set)


class ConfigDataDir(Config):
    """
    Datenordner
    """

    locked = False


    def set(self, value):
        """
        Schreibt die Datenordner-Konfiguration und alle davon abhängigen
        Konfigurationen nach *cherrypy.config*.
        Danach wird diese Einstellung für Änderungen gesperrt
        """

        # Keine Änderung erlaubt, wenn bereits gesperrt
        if self.locked:
            raise RuntimeError("Changing %s is not allowed" % self.name)

        # DATADIR
        cherrypy.config["DATADIR"] = value
        self.locked = True

        # DATAJSDIR
        cherrypy.config["DATAJSDIR"] = os.path.join(value, "js")

        # DATACSSDIR
        cherrypy.config["DATACSSDIR"] = os.path.join(value, "css")

        # DATATREEDIR
        cherrypy.config["DATATREEDIR"] = os.path.join(value, "tree")


    value = property(Config.get, set)


#
# Auflistung aller Konfigurationen
#
DATADIR = ConfigDataDir(
    u"DATADIR",
    u"Pfad zum Datenordner",
    (
        u"Vollständiger Pfad zum Ordner in dem alle Daten der CMS-Instanz "
        u"abgelegt sind. Diese Einstellung muss beim Start der Instanz "
        u"übergeben werden."
    )
)
DATAJSDIR = Config(
    u"DATAJSDIR",
    u"Pfad zum JavaScript-Ordner innerhalb des Datenordners",
    u"In diesem Ordner befinden sich benutzerdefinierte JavaScript-Dateien."
)
DATACSSDIR = Config(
    u"DATACSSDIR",
    u"Pfad zum CSS-Ordner innerhalb des Datenordners",
    u"In diesem Ordner befinden sich benutzerdefinierte CSS-Dateien."
)
DATATREEDIR = Config(
    u"DATATREEDIR",
    u"Pfad zum Baum-Ordner innerhalb des Datenordners",
    (
        u"Innerhalb dieses Ordners wird die gesamte Struktur des CMS abgebildet. "
        u"Jede Seite, jedes Bild und jeder Ordner der im CMS angezeigt wird, "
        u"befindet sich unterhalb dieses Ordners."
    )
)


