#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import string
import config


NOT_ALLOWED_FOLDERNAMES = {
    "interface",
}
NOT_ALLOWED_FILENAMES = NOT_ALLOWED_FOLDERNAMES.union({
    "settings.json"
})
ALLOWED_FOLDERNAME_CHARS = string.ascii_lowercase + string.digits + "_-"
NEW_DIR_MODE = 0777
NEW_FILE_MODE = 0666


# ToDo: Methode zum Löschen eines Ordners

# ToDo: Einstellungen eines Ordners per JSON-Datei speichern

# ToDo: History der Einstellungs-Änderungen speichern

# ToDo: Liste mit der Änderungshistorie eines Ordners zurück geben

# ToDo: Änderungen rückgängig machbar


# Globale Variable mit der Instanz des Datenbaumes; wird später befüllt;
tree = None


# Fehlerklassen
class DatadirError(RuntimeError): pass
class EmptyFoldername(DatadirError): pass
class NotAllowedCharInFoldername(DatadirError): pass
class NotAllowedFoldername(DatadirError): pass
class FolderAlreadyExists(DatadirError): pass
class FileAlreadyExists(DatadirError): pass


def init(datadir):
    """
    Initialisiert den Datenordner
    """

    global tree

    # Datenordner-Konfiguration setzen
    config.DATADIR.value = datadir

    # Benötigte Ordner erstellen
    create_main_dirs()

    # Oberste Ebene des Datenbaums laden
    tree = Folder(None, "")


def create_main_dirs():
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


class Folder(object):
    """
    Stellt den Datenordner dar, in dem alle Daten der CMS-Instanz abgelegt
    werden.

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
            self.path = config.DATADIR.value
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

        # Schlüssel sortieren
        self.sort_keys()

        # Fertig
        self.children_loaded = True


    def __getitem__(self, key):
        """
        __getitem__ wird überschrieben, um vorher die Unterordner
        einlesen zu können.

        :rtype: Folder
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
        return self.sorted_keys.__iter__()


    def __contains__(self, key):
        """
        __contains__ wird überschrieben, um vorher die Unterordner
        einlesen zu können.
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.data.__contains__(key)


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

        :rtype: list
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        return self.sorted_keys


    def items(self):
        """
        Items

        :rtype: list
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
        return self.sorted_keys.__iter__()


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

        :rtype: list
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

        :rtype: Folder
        """

        # Unterordner einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        if key not in self.data:
            return failobj
        return self.data[key]


    def sort_keys(self):
        """
        Schlüssel neu sortieren
        """

        self.sorted_keys = sorted(self.data)


    def new_item(self, name):
        """
        Erstellt einen neuen Unterordner und fügt diesen dem Dictionary
        hinzu.

        :return: Pfad zum neu erstellten Unterordner
        """

        # Name übernehmen, prüfen und Pfad zusammensetzen
        name = name.strip()
        if not name:
            raise EmptyFoldername()
        for char in name:
            if not char in ALLOWED_FOLDERNAME_CHARS:
                raise NotAllowedCharInFoldername(char)
        if name in NOT_ALLOWED_FOLDERNAMES:
            raise NotAllowedFoldername(name)
        path = os.path.join(self.path, name)

        # Prüfen ob der Ordner bereits existiert
        if os.path.isdir(path):
            raise FolderAlreadyExists(path)

        # Prüfen ob der Name als Datei bereits existiert
        if os.path.exists(path):
            raise FileAlreadyExists(path)

        # Ordner erstellen
        os.mkdir(path, NEW_DIR_MODE)

        # Neuen Ordner einlesen und Schlüssel sortieren
        self.data[name] = Folder(self, name)
        self.sort_keys()

        # Fertig
        return path





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






