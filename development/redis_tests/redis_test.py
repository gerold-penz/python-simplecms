# coding: utf-8

import os
import random
import string
import threading
import subprocess
import redis
import time
import logging


THISDIR = os.path.dirname(os.path.abspath(__file__))
REDIS_SERVER = "redis-server"
DATABASEDIR = os.path.join(THISDIR, "database")
DATABASESOCKET = os.path.join(DATABASEDIR, "redis-socket.sock")
DATABASEPASSWORD = "".join(
    random.choice(string.ascii_letters) for item in range(10)
)


REDIS_CONFIG = [
    'port 0',
    'bind 127.0.0.1',
    'unixsocket "%s"' % DATABASESOCKET,
    'unixsocketperm 700',
    'databases 1',
    'dbfilename "redis-data.rdb"',
    'dir "%s"' % DATABASEDIR,
    'appendonly yes',
    'appendfilename "redis-appendonly.aof"',
    'appendfsync everysec',
    'requirepass "%s"' % DATABASEPASSWORD,
]


def get_redis_connection():
    """
    Gibt eine fertig konfigurierte und getestete Redis-Connection zurück
    """

    for i in range(20):
        try:
            r = redis.StrictRedis(
                unix_socket_path = DATABASESOCKET,
                password = DATABASEPASSWORD
            )
            r.get("test")
            return r
        except redis.exceptions.ConnectionError, err:
            time.sleep(0.1)


class RedisServerThread(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)

        # Datenbankordner erstellen, falls dieser noch nicht existiert
        if not os.path.isdir(DATABASEDIR):
            os.makedirs(DATABASEDIR)

        self.daemonic = True
        self.stop_event = threading.Event()


    def run(self):
        """
        Threadfunktion in der der Redis-Server läuft
        """

        args = [REDIS_SERVER, "-"]
        proc = subprocess.Popen(
            args,
            executable = REDIS_SERVER,
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE
        )
        for line in REDIS_CONFIG:
            proc.stdin.write(line + "\n")

        # Warten bis gestoppt werden soll
        while not self.stop_event.is_set:
            time.sleep(0.2)

        # Fertig
        proc.stdin.close()


    def stop(self):
        """
        Stoppt den Redis-Server

        Übermittlung des SHUTDOWN-Kommandos und Stop-Event setzen
        """

        r = get_redis_connection()
        r.shutdown()
        self.stop_event.set()


def main():


    # Serverthread starten
    redis_thread = RedisServerThread()
    redis_thread.start()

    r = get_redis_connection()
    r.set("a", "b")
    print r.get("a")

    time.sleep(1)

    r.set("b", "c")
    print r.get("b")


    redis_thread.stop()
    redis_thread.join(timeout = 10000)


if __name__ == "__main__":
    main()











