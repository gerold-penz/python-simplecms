# coding: utf-8

import os
import sys
import cherrypy
import random
import string

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

DATABASEDIR = os.path.join(THISDIR, "database")
DATABASEFILENAME = "redis-data.rdb"
APPENDONLYFILENAME = "redis-appendonly.aof"
DATABASESOCKET = os.path.join(DATABASEDIR, "database.sock")
DATABASEPASSWORD = "".join(
    random.choice(string.ascii_letters) for item in range(10)
)


def main():

    # Datenbankordner erstellen, falls dieser noch nicht existiert
    if not os.path.isdir(DATABASEDIR):
        os.makedirs(DATABASEDIR)

    # Einstellungen für den Webserver
    config = {
        "global": {
            # Server settings
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 8080,
            # Redis settings
            "redis.server-cmd": "/usr/bin/redis-server",
            "redis.port": "0", # 6379
            "redis.bind": "127.0.0.1",
            "redis.unixsocket": DATABASESOCKET,
            "redis.unixsocketperm": "755",
            "redis.databases": 1,
            "redis.dbfilename": DATABASEFILENAME,
            "redis.dir": DATABASEDIR,
            "redis.requirepass": DATABASEPASSWORD,
            "redis.appendonly": "yes",
            "redis.appendfilename": APPENDONLYFILENAME,
            "redis.appendfsync": "everysec", # always, everysec, no
        },
        # "/": {
        # }
    }

    # Create and start application
    app = cherrypy.Application(None, config = config)
    cherrypy.quickstart(app, config = config)


if __name__ == "__main__":
    main()

