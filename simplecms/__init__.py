#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS

Hauptmodul

Created by Gerold - http://halvar.at/
"""

import os
import sys
import cherrypy
import logging
import constants
import config
import datadir
import http_root
from cherrypy import _cperror
from cherrypy import _cplogging
from logging import handlers


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
        data_root_dir,
        languages = None,
        script_name = "",
        additional_global_config = None,
        global_staticdir_match = (
            r"(?i)(gif|jpg|png|jpeg|js|7z|pdf|zip|svg|"
            r"emf|avi|ods|css|ico|html|htm|p3p|swf|htc)$"
        ),
        error_logfile_path = None,
        access_logfile_path = None
    ):
        """
        :param host: Hostname oder IP-Adresse an die der Server auf Anfragen
            horchen soll.

        :param port: Port-Nummer an der der Server auf Anfragen hochen soll.

        :param data_root_dir: Absoluter Pfad zum Ordner in dem sich alle Daten der
            "Simple Python CMS"-Instanz befinden. Existiert dieser Ordner nicht,
            wird er automatisch erstellt.

        :param languages: Liste mit den Sprachen in denen das CMS angezeigt
            werden soll. Standard: ["de"]

        :param additional_global_config: Zusätzlich zu den direkt übergebbaren
            Konfigurationsparametern, kann man ein Dictionary mit
            CherryPy-Konfigurationen für den "global"-Bereich übergeben.
            Details: siehe CherryPy-Hilfe

        :param global_staticdir_match: Sollte man Dateien mit Endungen ausliefern
            müssen, die nicht mit der vorgegebenen "Regular Expression"
            zu erfassen sind, kann man diesen Parameter überschreiben.
            Standard: (
                r"(?i)(gif|jpg|png|jpeg|js|7z|pdf|zip|svg|"
                r"emf|avi|ods|css|ico|html|htm|p3p|swf|htc)$"
            )

        :param error_logfile_path: Wenn angegeben, dann werden Fehler- und
            Statusmeldungen in diese Logdatei geschrieben.

        :param access_logfile_path: Wenn angegeben, dann werden
            Zugriffsmeldungen in diese Datei geschrieben
        """

        # Globale Konfigurationsparameter übernehmen
        config.DATAROOTDIR.value = data_root_dir
        config.DATABLOBSDIR.value = os.path.join(data_root_dir, "_blobs")
        config.DATACSSDIR.value = os.path.join(data_root_dir, "css")
        config.DATAJSDIR.value = os.path.join(data_root_dir, "js")
        config.DATATRASHDIR.value = os.path.join(data_root_dir, "_trash")
        config.LANGUAGES.value = languages

        # Pfade für Sprachen hinzufügen
        for lang in languages:
            setattr(http_root, lang, http_root)

        # Globale CherryPy-Konfiguration
        self.cherrypy_config = {
            "global": {
                # Einstellungen für den CherryPy-Standalone-Server
                "server.socket_host": host,
                "server.socket_port": port,
                # Produktivumgebung
                "environment": "production",
                "log.screen": False,
                "request.show_tracebacks": False,
                "request.show_mismatched_params": False,
                # Staticdir
                "tools.staticdir.root": constants.HTTPROOTDIR,
                # Gzip
                "tools.gzip.on": True,
                # Encoding der auszuliefernden HTML-Seiten
                "tools.encode.on": True,
                "tools.encode.encoding": "utf-8",
                "tools.decode.on": True,
                # URL Anpassung
                "tools.trailing_slash.on": True,
                # Custom-Tools
                #"tools.before_handler_tool.on": True,
            },
            "/": {
                # Staticdir
                "tools.staticdir.on": True,
                "tools.staticdir.dir": ".",
                "tools.staticdir.match": global_staticdir_match,
            }
        }
        if additional_global_config:
            self.cherrypy_config["global"].update(additional_global_config)

        # CherryPy-Anwendung initialisieren
        cherrypy.Application.__init__(
            self, http_root, script_name, self.cherrypy_config
        )

        # Rotated Error-Logging
        if error_logfile_path:
            error_logfile_path = os.path.abspath(error_logfile_path)

            # Falls der Ordner noch nicht existiert wird er erstellt
            error_logfile_dir = os.path.dirname(error_logfile_path)
            if not os.path.isdir(error_logfile_dir):
                os.makedirs(error_logfile_dir, 0770)

            # Logging in eine täglich rotierende Datei umleiten
            self.log.error_file = ""
            error_logfile_handler = handlers.TimedRotatingFileHandler(
                error_logfile_path,
                when = "midnight",
                interval = 1,
                backupCount = 9,
                encoding = "utf-8"
            )
            error_logfile_handler.setLevel(logging.DEBUG)
            error_logfile_handler.setFormatter(_cplogging.logfmt)
            self.log.error_log.addHandler(error_logfile_handler)

        # Rotated Access-Logging
        if access_logfile_path:
            access_logfile_path = os.path.abspath(access_logfile_path)

            # Falls der Ordner noch nicht existiert wird er erstellt
            access_logfile_dir = os.path.dirname(access_logfile_path)
            if not os.path.isdir(access_logfile_dir):
                os.makedirs(access_logfile_dir, 0770)

            # Logging in eine täglich rotierende Datei umleiten
            self.log.access_file = ""
            access_logfile_handler = handlers.TimedRotatingFileHandler(
                access_logfile_path,
                when = "midnight",
                interval = 1,
                backupCount = 9,
                encoding = "utf-8"
            )
            access_logfile_handler.setLevel(logging.DEBUG)
            access_logfile_handler.setFormatter(_cplogging.logfmt)
            self.log.access_log.addHandler(access_logfile_handler)

        # Datenordner initialisieren
        datadir.init()


    def start(self):
        """
        Startet den Webserver der Anwendung
        """

        # Web-Server starten
        cherrypy.quickstart(self, config = self.cherrypy_config)


# def before_handler_tool():
#     """
#     Diese Funktion wird ausgeführt, bevor der Request an den Request-Handler
#     weitergegeben wird
#     """
#
#     #
#     # Prüfen ob der Request über HTTPS gekommen ist.
#     # Damit kann Pound das HTTPS-Handling übernehmen
#     #
#     if "X-Ssl-Cipher" in cherrypy.request.headers:
#
#         # request.scheme
#         cherrypy.request.scheme = "https"
#
#         # wsgi.url_scheme
#         cherrypy.request.wsgi_environ["wsgi.url_scheme"] = "https"
#
#         # request.base
#         base_url = lib.http.Url(cherrypy.request.base)
#         base_url.scheme = "https"
#         cherrypy.request.base = unicode(base_url)
#
#
# cherrypy.tools.before_handler_tool = cherrypy.Tool(
#     "before_handler", before_handler_tool
# )
