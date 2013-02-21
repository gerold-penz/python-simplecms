#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS - Öffentlicher Root-Ordner

Created by Gerold 2013-02-21 http://halvar.at/
"""


def default(*args, **kwargs):
    """
    Diese Funktion wird ausgeführt, wenn es keine andere Funktion gibt, die
    den Request beantworten kann.

    Damit ist das die Funktion, über die fast jeder Seitenaufruf erfolgt.
    Zuerst wird versucht, den angeforderten Content aus dem DATATREEDIR
    zu holen. Wird dieser dort nicht gefunden, wird der angeforderte Content
    aus dem HTTPROOTDIR gelesen.
    """




    # Fertig
    return None

default.exposed = True

