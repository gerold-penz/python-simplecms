#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS

Hauptmodul

Created by Gerold - http://halvar.at/
"""

import cherrypy
import http_root
import lib.config
import lib.datadir


class SimpleCms(cherrypy.Application):
    """
    *Simple Python CMS*, abgeleitet von CherryPy-Application

    Da SimpleCms von *cherrypy.Application* abgeleitet wurde, ist SimpleCms
    eine vollwertige WSGI-Anwendung, die auch in einen Apache-Server mit
    *mod_wsgi* eingebunden werden kann.
    """

    def __init__(
        self,
        host,
        port,
        datadir,
        script_name = ""
    ):
        """
        :param host: Hostname oder IP-Adresse an die der Server auf Anfragen
            horchen soll.

        :param port: Port-Nummer an der der Server auf Anfragen hochen soll.

        :param datadir: Absoluter Pfad zum Ordner in dem sich alle Daten der
            "Simple Python CMS"-Instanz befinden. Existiert dieser Ordner nicht,
            wird er automatisch erstellt.
        """

        # Globale Konfiguration zusammensetzen
        self.global_config = {
            "global": {
                # Server settings
                "server.socket_host": host,
                "server.socket_port": port,
                # Datenordner
                "DATADIR": datadir
            },
        }

        # Anwendung initialisieren
        cherrypy.Application.__init__(
            self, http_root, script_name, self.global_config
        )

        # Datenordner initialisieren
        lib.datadir.init(datadir)


    def start(self):
        """
        Startet den Webserver der Anwendung
        """

        # Web-Server starten
        cherrypy.quickstart(self, config = self.global_config)




