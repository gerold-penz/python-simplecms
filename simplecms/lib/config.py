#!/usr/bin/env python
# coding: utf-8
"""
Konfigurationen

Über dieses Modul werden alle Grundkonfigurationen des Programmes gelesen

Die Grundkonfiguration ist in `cherrypy.config` gespeichert und darf nur
ausgelesen werden.

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import cherrypy


# ACHTUNG! Globales Dictionary mit allen Einstellungen
_global_all_configurations = {}


class Config(object):
    """
    Repräsentiert eine Konfiguration
    """

    def __init__(
        self,
        name,
        short_description,
        long_description = None,
        default = None
    ):

        global _global_all_configurations

        self.name = unicode(name)
        self.short_description = unicode(short_description)
        self.long_description = unicode(long_description) if long_description else None
        self.default = default

        # Einstellung in das globale Dict legen
        _global_all_configurations[name] = self


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


    __call__ = get
    value = property(get)



#
# Auflistung aller Konfigurationen
#
DATADIR = Config(
    u"DATADIR",
    u"Pfad zum Datenordner",
    (
        u"Vollständiger Pfad zum Ordner in dem alle Daten der CMS-Instanz "
        u"abgelegt sind. Diese Einstellung muss beim Start der Instanz "
        u"übergeben werden."
    )
)





