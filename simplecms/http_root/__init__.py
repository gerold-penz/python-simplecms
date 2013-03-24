#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS - Öffentlicher Root-Ordner

Created by Gerold 2013-02-21 http://halvar.at/
"""

from simplecms import datadir


def default(*args, **kwargs):
    """
    Diese Funktion wird ausgeführt, wenn es keine andere Funktion gibt, die
    den Request beantworten kann.

    Damit ist *default* die Funktion, über die fast jeder Seitenaufruf erfolgt.
    Zuerst wird versucht, den angeforderten Content aus dem DATAROOTDIR
    zu holen. Wird dieser dort nicht gefunden, wird der angeforderte Content
    aus dem HTTPROOTDIR gelesen.

    :param args: Pfadsegmente in einer Liste

    :param kwargs: Benannte Parameter (Query-String) als Dictionary
    """

    # Pfad zusammensetzen
    path = "/" + "/".join(args)

    # Im Datenbaum nachsehen, ob es den zugehörigen Ordner gibt.
    node = datadir.find_path(path)
    if node:
        return repr((
            node["de_at"].content,
            node["de_de"].content,
            node["de"].content,
            node["auto"].content,
        ))



    # ToDo: Im http_root nachsehen, ob es den zugehörigen Ordner gibt.


    # ToDo: Prüfen ob es Content gibt, der angezeigt werden kann.














    import pprint
    return pprint.pformat(args) + "\n\n" + pprint.pformat(kwargs)


    # Fertig
    return u"DEFAULT"

default.exposed = True


def testseite(*args, **kwargs):
    """
    Testseite

    Wird zum Entwickeln benötigt um ab und zu eine Funktion zu testen
    """

    basenode = datadir.basenode
    assert isinstance(basenode, datadir.Node)

    # for key, value in tree.iteritems():
    #     print key
    #     for subkey, subvalue in value.items():
    #         print "  ", subkey
    #
    #
    # for key in tree.iterkeys():
    #     print key


    print
    print basenode.nodedir_path
    print




    # Fertig
    return u"TESTSEITE"

testseite.exposed = True
