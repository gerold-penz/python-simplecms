#!/usr/bin/env python
# coding: utf-8
"""
Cookie
"""

import cherrypy
import cookielib
import time


LANGUAGE = "L"


def get_cookie(key):
    """
    Liest den Wert des angegebenen Cookies aus dem **Request**.
    """

    cookie = cherrypy.request.cookie.get(key, None)

    if cookie:
        return cookie.value
    else:
        return None


def set_cookie(key, value, path = "/", expires_days = 60):
    """
    Schreibt das Cookie in den **Response**.
    """

    cookie = cherrypy.response.cookie

    # Cookie setzen
    cookie[key] = value
    cookie[key]["path"] = "/"
    expires = time.time() + (expires_days * 24 * 60 * 60)
    cookie[key]["expires"] = cookielib.time2netscape(expires)


def del_cookie(key, path = "/"):
    """
    Löscht das Cookie.
    """

    # Cookie löschen
    set_cookie(key, value = "", path = path, expires_days = -1000)

