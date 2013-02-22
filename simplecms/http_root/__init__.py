#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS - Öffentlicher Root-Ordner

Created by Gerold 2013-02-21 http://halvar.at/
"""

from simplecms.lib import datadir


def default(*args, **kwargs):
    """
    Diese Funktion wird ausgeführt, wenn es keine andere Funktion gibt, die
    den Request beantworten kann.

    Damit ist *default* die Funktion, über die fast jeder Seitenaufruf erfolgt.
    Zuerst wird versucht, den angeforderten Content aus dem DATATREEDIR
    zu holen. Wird dieser dort nicht gefunden, wird der angeforderte Content
    aus dem HTTPROOTDIR gelesen.

    :param args: Pfadsegmente in einer Liste

    :param kwargs: Benannte Parameter (Query-String) als Dictionary
    """

    # Datenbaum
    tree = datadir.tree
    assert isinstance(tree, datadir.Folder)




    # ToDo: Zuerst im Datenordner nachsehen, ob es den zugehörigen Ordner gibt.









    import pprint
    return pprint.pformat(args) + "\n\n" + pprint.pformat(kwargs)


    # Fertig
    return u"DEFAULT"

default.exposed = True

