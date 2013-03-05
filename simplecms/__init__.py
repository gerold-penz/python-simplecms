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
import constants
import config
import datadir
import http_root


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
        )
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

        """

        # Globale Konfigurationsparameter übernehmen
        config.DATAROOTDIR.value = data_root_dir
        config.DATABLOBSDIR.value = os.path.join(data_root_dir, "_blobs")
        config.DATACSSDIR.value = os.path.join(data_root_dir, "css")
        config.DATAJSDIR.value = os.path.join(data_root_dir, "js")
        config.DATATRASHDIR.value = os.path.join(data_root_dir, "_trash")
        config.LANGUAGES.value = languages

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

        # Datenordner initialisieren
        datadir.init()




        # # TESTS
        # basenode = datadir.basenode
        # basenode.find("/asdf/asdf")
        #
        # basenode = datadir.basenode
        # assert isinstance(basenode, datadir.Node)
        #
        # print
        # print tree.visible
        # print tree["de"].title
        # print tree["en"].title
        # print tree["de"].description
        #
        # # tree.child("hallo").child("servus").child("test")
        # # tree.children["hallo"].children[""]
        # # node = datadir.search("/") tree.query("/")


        basenode = datadir.basenode
        assert isinstance(basenode, datadir.Node)

        print
        print basenode
        print basenode.children["test1"]

        # for key, child in basenode.children.items():
        #     assert isinstance(child, datadir.Node)
        #     print child
        #     for subchild in child.children.values():
        #         print subchild
        #
        # print



    def start(self):
        """
        Startet den Webserver der Anwendung
        """

        # Web-Server starten
        cherrypy.quickstart(self, config = self.cherrypy_config)




