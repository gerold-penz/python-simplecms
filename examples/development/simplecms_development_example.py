# coding: utf-8

import os
import sys
import cherrypy

THISDIR = os.path.dirname(os.path.abspath(__file__))

try:
    import simplecms
except ImportError:
    # SIMPLECMSDIR und `sys.path.insert` werden nur zum Testen benötigt.
    # Wenn `simplecms` installiert wurde, kann man es einfach importieren,
    # ohne vorher den Pfad angeben zu müssen.
    SIMPLECMSDIR = os.path.abspath(os.path.join(THISDIR, "..", ".."))
    sys.path.insert(0, SIMPLECMSDIR)
    import simplecms


def main():

    # Einstellungen für den Webserver
    config = {
        "global": {
            # Server settings
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 8080,
        },
        # "/": {
        # }
    }

    # Create and start application
    app = cherrypy.Application(None, config = config)
    cherrypy.quickstart(app, config = config)


if __name__ == "__main__":
    main()

