#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import string
import config


NOT_ALLOWED_FOLDERNAMES = {"js", "css", "interface", "tree"}
ALLOWED_FOLDERNAME_CHARS = string.ascii_letters + string.digits + "_-"


# ACHTUNG! Globale Variable mit der Instanz des Datenbaumes
tree = None


def init(datadir):
    """
    Initialisiert den Datenordner
    """

    global tree

    # Datenordner-Konfiguration setzen
    config.DATADIR.value = datadir

    # Benötigte Ordner erstellen
    create_dirs()

    # Oberste Ebene des Datenbaums laden
    tree = Folder(None, "")


def create_dirs():
    """
    Erstellt den Datenordner und die benötigten Unterordner,
    falls diese noch nicht existieren.
    """

    # Hauptordner
    datadir = config.DATADIR.value
    assert datadir
    if not os.path.isdir(datadir):
        os.makedirs(datadir)

    # JavaScript-Ordner
    datajsdir = config.DATAJSDIR.value
    if not os.path.isdir(datajsdir):
        os.makedirs(datajsdir)

    # CSS-Ordner
    datacssdir = config.DATACSSDIR.value
    if not os.path.isdir(datacssdir):
        os.makedirs(datacssdir)

    # Datenbaum-Ordner
    datatreedir = config.DATATREEDIR.value
    if not os.path.isdir(datatreedir):
        os.makedirs(datatreedir)


class Folder(object):
    """
    Stellt einen Datenordner innerhalb von DATATREEDIR dar

    Die Daten liegen in einem Dictionary. Ein Folder-Objekt besitzt ähnliche
    Methoden wie ein Dictionary. Die Rückgabe von Listen oder Iteratoren
    wird vorher alphabetisch sortiert.
    """

    def __init__(self, parent, name):
        """
        Initialisiert den Datenordner

        :param parent: Eltern-Ordner als DataFolder-Objekt
            Wird `None` übergeben, dann gibt es keinen übergeordneten Ordner

        :param name: Name des Ordners. Wird ein leerer String übergeben, dann
            handelt es sich um den obersten Datenordner
        """

        assert (not parent and not name) or (not parent is None and name)

        self.data = {}
        self.parent = parent
        self.name = name
        if self.parent:
            self.path = os.path.join(self.parent.path, self.name)
        else:
            self.path = config.DATATREEDIR.value
        self.children_loaded = False
        self.sorted_keys = []


    def load_children(self, force = False):
        """
        Läd die Unterordner nach.

        Die Unterordner werden erst dann geladen, wenn sie benötigt werden.

        :param force: Wenn `True`, dann werden die Unterordner nochmal geladen,
            auch wenn diese bereits geladen wurden.
        """

        # Erzwungenes Neuladen der Unterordner
        if force:
            self.children_loaded = False

        # Abbrechen, wenn bereits geladen
        if self.children_loaded:
            return

        # Alle Kindelemente löschen
        self.data.clear()

        # Alle Unterordner in das Dictionary legen
        for dirpath, dirnames, filenames in os.walk(self.path):
            for dirname in dirnames:
                self.data[dirname] = Folder(parent = self, name = dirname)
            break

        # Sorted Keys
        self.sorted_keys = sorted(self.data)

        # Fertig
        self.children_loaded = True


    def __getitem__(self, key):
        """
        __getitem__ wird überschrieben, um vorher die Unterordner
        einlesen zu können.
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.data.__getitem__(key)


    def __setitem__(self, key, value):
        """
        __setitem__ wird überschrieben, da ein direktes Befüllen der
        Unterordner nicht erlaub ist.
        """

        raise RuntimeError("__setitem__ not allowed")


    def __delitem__(self, key):
        """
        __delitem__ wird überschrieben, da ein direktes Löschen der
        Unterordner nicht erlaubt ist.
        """

        raise RuntimeError("__delitem__ not allowed")


    def __iter__(self):
        """
        __iter__ wird überschrieben, um vorher die Unterordner
        einlesen zu können.
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        for key in self.sorted_keys:
            yield key


    def __contains__(self, key):
        """
        __contains__ wird überschrieben, um vorher die Unterordner
        einlesen zu können.
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return key in self.data


    def has_key(self, key):
        """
        *has_key* wird überschrieben, um vorher die Unterordner
        einlesen zu können.
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.data.has_key(key)


    def __repr__(self):
        """
        Gibt die String-Repräsentation des Folder-Objektes zurück
        """

        return "Folder('%s')" % self.name


    def __cmp__(self, folder):
        """
        Vergleich
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Vergleichen und zurück geben
        if isinstance(folder, Folder):
            return cmp(self.data, folder.data)
        else:
            return cmp(self.data, folder)


    def keys(self):
        """
        Gibt die Namen der Unterordner zurück
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        return self.sorted_keys


    def items(self):
        """
        Items
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        retlist = []
        for key in self.sorted_keys:
            retlist.append((key, self.data[key]))
        return retlist


    def iteritems(self):
        """
        Iteritems
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        for key in self.sorted_keys:
            yield (key, self.data[key])


    def iterkeys(self):
        """
        Iterkeys
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        for key in self.sorted_keys:
            yield key


    def itervalues(self):
        """
        Itervalues
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        for key in self.sorted_keys:
            yield self.data[key]


    def values(self):
        """
        Values
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        retlist = []
        for key in self.sorted_keys:
            retlist.append(self.data[key])
        return retlist


    def get(self, key, failobj = None):
        """
        Get
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        if key not in self.data:
            return failobj
        return self.data[key]


# def get_tree():
#     """
#     Gibt das Tree-Objekt zurück.
#
#     Helferlein für PyCharm, damit die Code-Vervollständigung funktioniert
#
#     :rtype: Folder
#     """
#
#     return tree






