#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import io
import string
import config
try:
    import jsonlib2 as json
except ImportError:
    import json


# Regeln für neue Nodes bzw. Dateien
NOT_ALLOWED_NODENAMES = {"interface"}
NOT_ALLOWED_FILENAMES = NOT_ALLOWED_NODENAMES.union({"metadata.json"})
ALLOWED_NODENAME_CHARS = string.ascii_lowercase + string.digits + "_-"
NEW_DIR_MODE = 0770
NEW_FILE_MODE = 0660


# ToDo: Content eines Nodes in den verschiedenen Sprachen mit Snappy komprimiert speichern

# ToDo: History der Einstellungs-Änderungen speichern

# ToDo: Liste mit der Änderungshistorie eines Ordners zurück geben

# ToDo: Änderungen rückgängig machbar

# ToDo: Methode zum Löschen eines Ordners


# Globale Variable mit der Instanz des Datenbaumes; wird später befüllt;
tree = None


# Fehlerklassen
class DatadirError(RuntimeError): pass
class EmptyNodeName(DatadirError): pass
class NotAllowedCharInNodeName(DatadirError): pass
class NotAllowedNodeName(DatadirError): pass
class NodeAlreadyExists(DatadirError): pass
class FileAlreadyExists(DatadirError): pass


# Globale Liste mit den Metadaten
all_metadata_names = set()


class Metadata(property):
    """
    Metadaten Property-Klasse
    """

    def __init__(self, *args, **kwargs):
        """
        Sammelt die Liste aller Metadaten
        """

        property.__init__(self, *args, **kwargs)

        # Namen der Getter-Funktion zur Liste der Metadaten hinzufügen
        all_metadata_names.add(args[0].__name__)


def init(data_root_dir):
    """
    Initialisiert den Datenordner
    """

    global tree

    # Datenordner-Konfiguration setzen
    config.DATAROOTDIR.value = data_root_dir

    # Benötigte Ordner erstellen
    create_main_dirs()

    # Oberste Ebene des Datenbaums laden
    tree = Node(None, "")


def create_main_dirs():
    """
    Erstellt den Datenordner und die benötigten Unterordner,
    falls diese noch nicht existieren.
    """

    # Hauptordner
    data_root_dir = config.DATAROOTDIR.value
    assert data_root_dir
    if not os.path.isdir(data_root_dir):
        os.makedirs(data_root_dir)

    # JavaScript-Ordner
    datajsdir = config.DATAJSDIR.value
    if not os.path.isdir(datajsdir):
        os.makedirs(datajsdir)

    # CSS-Ordner
    datacssdir = config.DATACSSDIR.value
    if not os.path.isdir(datacssdir):
        os.makedirs(datacssdir)


class Node(object):
    """
    Stellt einen Datenordner-Knoten dar.

    Die Daten liegen in einem Dictionary. Ein Node-Objekt besitzt ähnliche
    Methoden wie ein Dictionary. Die Rückgabe von Listen oder Iteratoren
    wird vorher alphabetisch sortiert.
    """

    def __init__(self, parent, name):
        """
        Initialisiert den Datenknoten

        :param parent: Eltern-Knoten als Node-Objekt
            Wird `None` übergeben, dann gibt es keinen übergeordneten Datenknoten

        :param name: Name des Knotens. Wird ein leerer String übergeben, dann
            handelt es sich um den obersten Datenknoten
        """

        assert (not parent and not name) or (not parent is None and name)

        self.children = {}
        self.parent = parent
        self.name = name
        if self.parent:
            self.path = os.path.join(self.parent.path, self.name)
        else:
            self.path = config.DATAROOTDIR.value
        self.metadata_path = os.path.join(self.path, "metadata.json")
        self.children_loaded = False
        self.sorted_keys = []
        self.metadata_items = {}


        # Metadaten laden
        self.load_metadata()


    def load_metadata(self):
        """
        Läd die Metadaten und bindet sie an den Node

        Die Metadaten selbst sind Attribute dieser Klasse.
        """

        metadata = {}
        if os.path.isfile(self.metadata_path):
            with io.open(self.metadata_path, "rb") as metadata_file:
                metadata = json.loads(metadata_file.read()) or {}
        for metadata_key in all_metadata_names:
            self.metadata_items[metadata_key] = metadata.get(metadata_key)


    def save_metadata(self):
        """
        Speichert die Metadaten
        """

        metadata = {}
        for metadata_key in all_metadata_names:
            metadata[metadata_key] = getattr(self, metadata_key, None)
        with io.open(self.metadata_path, "wb") as metadata_file:
            json.dump(metadata, metadata_file, indent = 0)


    def load_children(self, force = False):
        """
        Läd die Unterknoten nach.

        Die Unterknoten werden erst dann geladen, wenn sie benötigt werden.

        :param force: Wenn `True`, dann werden die Unterknoten nochmal geladen,
            auch wenn diese bereits geladen wurden. Normalerweise werden
            die Unterknoten nur ein einziges mal geladen. Egal wie oft diese
            Methode aufgerufen wird.
        """

        # Erzwungenes Neuladen der Unterknoten
        if force:
            self.children_loaded = False

        # Abbrechen, wenn bereits geladen
        if self.children_loaded:
            return

        # Alle Kindelemente löschen
        self.children.clear()

        # Alle Unterknoten in das Dictionary legen
        for dirpath, dirnames, filenames in os.walk(self.path):
            for dirname in dirnames:
                self.children[dirname] = Node(parent = self, name = dirname)
            break

        # Schlüssel sortieren
        self.sort_keys()

        # Fertig
        self.children_loaded = True


    def __getitem__(self, key):
        """
        Gibt den gewünschten Unterknoten zurück

        :rtype: Node
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.children.__getitem__(key)


    # def __setitem__(self, key, value):
    #     """
    #     __setitem__ wird überschrieben, da ein direktes Befüllen der
    #     Unterknoten nicht erlaub ist.
    #     """
    #
    #     raise RuntimeError("__setitem__ not allowed")


    # def __delitem__(self, key):
    #     """
    #     __delitem__ wird überschrieben, da ein direktes Löschen der
    #     Unterknoten nicht erlaubt ist.
    #     """
    #
    #     raise RuntimeError("__delitem__ not allowed")


    def __iter__(self):

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.sorted_keys.__iter__()


    def __contains__(self, key):

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.children.__contains__(key)


    def has_key(self, key):

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Rückgabe
        return self.children.has_key(key)


    def __repr__(self):

        return "Node('%s')" % self.name


    def __cmp__(self, node):

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Vergleichen und zurück geben
        if isinstance(node, Node):
            return cmp(self.children, node.children)
        else:
            return cmp(self.children, node)


    def keys(self):
        """
        Gibt die Namen der Unterknoten zurück

        :rtype: list
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        return self.sorted_keys


    def items(self):
        """
        Gibt die Unterknoten-Namen und -Objekte zurück

        :rtype: list
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        retlist = []
        for key in self.sorted_keys:
            retlist.append((key, self.children[key]))
        return retlist


    def iteritems(self):
        """
        Gibt die Unterknoten-Namen und -Objekte zurück
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        for key in self.sorted_keys:
            yield (key, self.children[key])


    def iterkeys(self):
        """
        Gibt die Namen der Unterknoten zurück
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        return self.sorted_keys.__iter__()


    def itervalues(self):
        """
        Gibt die Unterknoten-Objekte zurück
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        for key in self.sorted_keys:
            yield self.children[key]


    def values(self):
        """
        Gibt die Unterknoten-Objekte zurück

        :rtype: list
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        retlist = []
        for key in self.sorted_keys:
            retlist.append(self.children[key])
        return retlist


    def get(self, key, failobj = None):
        """
        Gibt den gewünschten Unterknoten zurück

        :rtype: Node
        """

        # Unterknoten einlesen falls noch nicht geladen
        self.load_children()

        # Fertig
        if key not in self.children:
            return failobj
        return self.children[key]


    def sort_keys(self):
        """
        Schlüssel der Unterknoten neu sortieren
        """

        self.sorted_keys = sorted(self.children)


    def new_item(self, name):
        """
        Erstellt einen neuen Unterordner im Dateisystem und fügt diesen dem
        Dictionary mit den Unterknoten hinzu.

        :return: Pfad zum neu erstellten Unterknoten
        """

        # Name übernehmen, prüfen und Pfad zusammensetzen
        name = name.strip()
        if not name:
            raise EmptyNodeName()
        for char in name:
            if not char in ALLOWED_NODENAME_CHARS:
                raise NotAllowedCharInNodeName(char)
        if name in NOT_ALLOWED_NODENAMES:
            raise NotAllowedNodeName(name)
        path = os.path.join(self.path, name)

        # Prüfen ob der Ordner bereits existiert
        if os.path.isdir(path):
            raise NodeAlreadyExists(path)

        # Prüfen ob der Name als Datei bereits existiert
        if os.path.exists(path):
            raise FileAlreadyExists(path)

        # Ordner erstellen
        os.mkdir(path, NEW_DIR_MODE)

        # Neuen Ordner einlesen und Schlüssel sortieren
        self.children[name] = Node(self, name)
        self.sort_keys()

        # Fertig
        return path


    @Metadata
    def title(self):
        return self.metadata_items.get("title")


    @title.setter
    def title(self, value):
        self.metadata_items["title"] = value
        # Speichern
        self.save_metadata()


    @Metadata
    def visible(self):
        return self.metadata_items.get("visible")


    @visible.setter
    def visible(self, value):
        self.metadata_items["visible"] = value
        # Speichern
        self.save_metadata()


