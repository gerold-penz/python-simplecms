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

    # Datenbaum
    tree = datadir.tree
    assert isinstance(tree, datadir.Node)






    # ToDo: Zuerst im Datenbaum nachsehen, ob es den zugehörigen Ordner gibt.


    # ToDo: Danach im http_root nachsehen, ob es den zugehörigen Ordner gibt.


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

    tree = datadir.tree
    assert isinstance(tree, datadir.Node)

    # for key, value in tree.iteritems():
    #     print key
    #     for subkey, subvalue in value.items():
    #         print "  ", subkey
    #
    #
    # for key in tree.iterkeys():
    #     print key


    print
    print tree.title
    print


    tree.title = u"Wir sind gekommen um zu bleiben"


    # Fertig
    return u"TESTSEITE"

testseite.exposed = True
