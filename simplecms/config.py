#!/usr/bin/env python
# coding: utf-8
"""
Grundkonfigurationen des Programmes lesen und initialisieren

Die Grundeinstellungen werden beim Start der Anwendung ermittelt und dürfen
im laufenden Betrieb nicht mehr verändert werden.

Created 2013-02-21 by Gerold - http://halvar.at/
"""

# Dictionary mit allen Einstellungen
all_configurations = {}


class Config(object):
    """
    Repräsentiert eine Konfiguration
    """

    locked = False
    _value = None


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
        Gibt den Wert der Konfiguration zurück
        """

        if self._value is None:
            return self.default
        else:
            return self._value


    def set(self, value):
        """
        Setzt den Wert der Konfiguration
        """

        if self.locked:
            raise RuntimeError("Changing %s is not allowed" % self.name)
        self._value = value
        self.locked = True


    value = property(get, set)


#
# Auflistung aller Konfigurationen
#
DATAROOTDIR = Config(
    u"DATAROOTDIR",
    u"Pfad zum Datenordner",
    (
        u"Vollständiger Pfad zum Ordner in dem alle Daten der CMS-Instanz "
        u"abgelegt sind. Diese Einstellung muss beim Start der Instanz "
        u"übergeben werden. "
        u"Innerhalb dieses Ordners wird die gesamte Struktur des CMS abgebildet. "
        u"Jede Seite, jedes Bild und jeder Ordner der im CMS angezeigt wird, "
        u"befindet sich unterhalb dieses Ordners."
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
DATABLOBSDIR = Config(
    u"DATABLOBSDIR",
    u"Pfad zum Blobs-Ordner innerhalb des Datenordners",
    u"In diesem Ordner befinden sich die mit Snappy komprimierten BLOB-Dateien."
)
DATATRASHDIR = Config(
    u"DATATRASHDIR",
    u"Pfad zum Trash-Ordner innerhalb des Datenordners",
    u"In diesem Ordner befinden sich die gelöschten Nodes."
)
LANGUAGES = Config(
    u"LANGUAGES",
    u"Sprachen",
    u"Liste mit den Sprachen in denen das CMS die Inhalte zeigt",
    default = ["de", "en"]
)

