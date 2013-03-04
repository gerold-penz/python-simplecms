#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import io
import re
import string
import glob
import config
try:
    import jsonlib2 as json
except ImportError:
    import json


# Regeln für neue Nodes bzw. Dateien
NOT_ALLOWED_NODENAMES = {"interface", "_data", "_blobs", "_trash"}
#ALLOWED_NODENAME_CHARS = string.ascii_lowercase + string.digits + "_-"
#NEW_DIR_MODE = 0770
#NEW_FILE_MODE = 0660


# ToDo: Blobs mit Snappy komprimiert speichern

# ToDo: History der Einstellungs-Änderungen speichern

# ToDo: Liste mit der Änderungshistorie eines Ordners zurück geben

# ToDo: Änderungen rückgängig machbar

# ToDo: Methode zum Löschen eines Ordners --> in den *_trash_*-Ordner


# Globale Variable mit der Instanz des obesten Nodes; wird später befüllt;
basenode = None

# Globales Dictionary mit allen eingelesenen Knoten
_all_loaded_nodes = {}


# Fehlerklassen
class DatadirError(RuntimeError): pass
class EmptyNodeName(DatadirError): pass
class NotAllowedCharInNodeName(DatadirError): pass
class NotAllowedNodeName(DatadirError): pass
class NodeAlreadyExists(DatadirError): pass
class FileAlreadyExists(DatadirError): pass


def init():
    """
    Initialisiert den Datenordner
    """

    global basenode

    # Benötigte Ordner erstellen
    create_main_dirs()

    # Oberste Ebene des Datenbaums laden
    basenode = Node()


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

    # Blobs-Ordner
    datablobsdir = config.DATABLOBSDIR.value
    if not os.path.isdir(datablobsdir):
        os.makedirs(datablobsdir)

    # CSS-Ordner
    datacssdir = config.DATACSSDIR.value
    if not os.path.isdir(datacssdir):
        os.makedirs(datacssdir)

    # JavaScript-Ordner
    datajsdir = config.DATAJSDIR.value
    if not os.path.isdir(datajsdir):
        os.makedirs(datajsdir)

    # Trash-Ordner
    datatrashdir = config.DATATRASHDIR.value
    if not os.path.isdir(datatrashdir):
        os.makedirs(datatrashdir)


def find_url(url):
    """
    Gibt den Knoten zurück, der der übergebenen URL entspricht

    :param url: URL zum Datenknoten. Dieser muss *immer* mit einem "/"
        beginnen.

    :rtype: Node
    """

    # Parameter
    url = url.strip()
    assert url.startswith("/")
    url = "/" + url.lstrip("/").rstrip("/")

    # Schnelle Rückgabe, falls der gewünschte Knoten bereits eingelesen wurde
    if url in _all_loaded_nodes:
        return _all_loaded_nodes[url]

    # Suche
    current_node = basenode
    for urlpart in url.split("/")[1:]:
        assert isinstance(current_node, Node)
        current_node = current_node.children.get(urlpart)
        if not current_node:
            return

    # Rückgabe
    return current_node or None


class Node(dict):
    """
    Repräsentiert einen Datenordner/Knoten

    Die Sprachabhängigen Daten sind im Dictionary hinterlegt

    Hinweis für Programmierer: Es wäre normalerweise nicht notwendig,
    die Attribute gemeinsam mit Datenschlüssel (all_data_keys) doppelt
    mitzuführen. Das ist der IDE (PyCharm) geschuldet, damit die
    Codevervollständigung dabei hilft Fehler beim Programmieren zu vermeiden.
    """

    # Children
    _children = None

    # Daten-Attribute
    # (zusammenpassend zu den Datenschlüsseln)
    visible = False

    # Liste mit den Datenschlüsseln
    # (zusammenpassend mit den Daten-Attributen)
    all_data_keys = [
        "visible",
    ]


    class LangData(object):
        """
        Repräsentiert die sprachabhängigen Daten eines Nodes

        Hinweis für Programmierer: Es wäre normalerweise nicht notwendig,
        die Attribute gemeinsam mit Datenschlüssel (all_data_keys) doppelt
        mitzuführen. Das ist der IDE (PyCharm) geschuldet, damit die
        Codevervollständigung dabei hilft Fehler beim Programmieren zu vermeiden.
        """

        # Sprachabhängige Daten-Attribute
        # (zusammenpassend zu den Datenschlüsseln)
        title = None
        menu = None
        description = None
        keywords = None
        html = None

        # Liste mit den sprachabhängigen Datenschlüsseln
        # (zusammenpassend mit den Daten-Attributen)
        all_data_keys = [
            "title",
            "menu",
            "description",
            "keywords",
            "html",
        ]


    def __init__(self, parent = None, name = "/"):
        """
        Initialisiert den Datenknoten

        :param parent: Eltern-Knoten als Node-Objekt
            Wird `None` übergeben, dann gibt es keinen übergeordneten Datenknoten

        :param name: Name des Knotens. Wird ein leerer String oder "/" übergeben,
            dann handelt es sich um den obersten Datenknoten
        """

        dict.__init__(self)

        # Parameter
        self.name = name = name or "/"
        self.parent = parent
        assert (not parent and name == "/") or (not parent is None and name != "/")

        # Url
        if self.parent:
            self.url = self.parent.url.rstrip("/") + "/" + self.name.rstrip("/")
        else:
            self.url = self.name

        # Klasseninstanz in das globale Dictionary legen
        _all_loaded_nodes[self.url] = self

        # Pfade festlegen
        if self.parent:
            self.nodedir_path = os.path.join(self.parent.nodedir_path, self.name)
        else:
            self.nodedir_path = config.DATAROOTDIR.value
        self.datadir_path = os.path.join(self.nodedir_path, "_data")
        self.datadir_current_path = os.path.join(self.datadir_path, "current")
        self.datadir_archive_path = os.path.join(self.datadir_path, "archive")

        # Daten je Sprache
        for language_id in config.LANGUAGES.value:
            self[language_id] = self.LangData()

        # Daten laden
        self.load()


    def __getitem__(self, language):
        """
        Gibt die Daten der übergebenen Sprache zurück

        :rtype: LangData
        """

        return dict.__getitem__(self, language)


    def load(self):
        """
        Läd die Daten aus dem Dateisystem
        """

        # Neueste JSON-Datei ermitteln
        filelist = glob.glob(os.path.join(self.datadir_current_path, "*.json"))
        if not filelist:
            return
        datafile_path = os.path.abspath(sorted(filelist)[-1])

        # JSON-Datei laden
        with io.open(datafile_path, "rb") as datafile:
            loaded_data = json.loads(datafile.read())
        if not loaded_data:
            return

        # Sprachunabhängige Daten aus der JSON-Datei zur Klasseninstanz hinzufügen
        for data_key in self.all_data_keys:
            setattr(
                self,
                data_key,
                loaded_data.get(data_key, getattr(self, data_key))
            )

        # Sprachabhängige Daten aus der JSON-Datei zu den
        # sprachabhängigen Klasseninstanzen hinzufügen
        for language_id, language_data in self.items():
            assert isinstance(language_data, self.LangData)
            for data_key in language_data.all_data_keys:
                setattr(
                    language_data,
                    data_key,
                    loaded_data.get(data_key, {}).get(
                        language_id,
                        getattr(language_data, data_key)
                    )
                )


    def save(self):
        """
        Speichert die Daten ins Dateisystem
        """

        # ToDo:

        # metadata = {}
        # for metadata_key in all_metadata_names:
        #     metadata[metadata_key] = getattr(self, metadata_key, None)
        # with io.open(self.metadata_path, "wb") as metadata_file:
        #     json.dump(metadata, metadata_file, indent = 0)


    def __repr__(self):
        """
        __repr__
        """

        # Repräsentation der Node-Klasse auslesen
        match = re.search(u"'(.*?)'", unicode(self.__class__), re.UNICODE)
        if match:
            class_repr = unicode(match.groups()[0])
        else:
            class_repr = "Node"

        # Rückgabe des Klassennamens und des Node-Namens
        return "<%s '%s'>" % (class_repr, self.url)


    @property
    def children(self):
        """
        Gibt ein Dictionary-artiges Objekt mit den Subnodes/Unterordnern zurück

        Die Informationen über die Unterknoten werden beim ersten Zugriff
        auf *Node.children* aus dem Dateisystem eingelesen.

        :rtype: Children
        """

        # Unterordner einlesen, falls diese noch nicht eingelesen wurden
        if self._children is None:
            self._children = self.Children(self)

        # Children zurück liefern
        return self._children


    class Children(dict):
        """
        Repräsentiert ein Dictionary-artiges Objekt mit den
        Subnodes/Unterordnern eines Knotens
        """

        def __init__(self, parent):
            """
            Init
            """

            dict.__init__(self)
            assert isinstance(parent, Node)
            self.parent = parent
            self.sorted_keys = []
            self.load()


        def load(self):
            """
            Läd die Unterknoten aus dem Dateisystem
            """

            # Alle Kindelemente löschen
            dict.clear(self)

            # Alle (erlaubten) Unterknoten in das Dictionary legen
            for dirpath, dirnames, filenames in os.walk(self.parent.nodedir_path):
                for dirname in dirnames:
                    if dirname not in NOT_ALLOWED_NODENAMES:
                        dict.__setitem__(
                            self,
                            dirname,
                            Node(parent = self.parent, name = dirname)
                        )
                break

            # Schlüssel sortieren
            self.sort_keys()


        def sort_keys(self):
            """
            Schlüssel der Unterknoten neu sortieren
            """

            self.sorted_keys = sorted(dict.keys(self))


        def __getitem__(self, key):
            """
            Gibt den gewünschten Unterknoten zurück

            :rtype: Node
            """

            return dict.__getitem__(self, key)


        def __setitem__(self, key, value):
            """
            __setitem__ wird überschrieben, da ein direktes Befüllen der
            Unterknoten nicht erlaub ist.
            """

            raise RuntimeError("__setitem__ not allowed")


        def __delitem__(self, key):
            """
            __delitem__ wird überschrieben, da ein direktes Löschen der
            Unterknoten nicht erlaubt ist.
            """

            raise RuntimeError("__delitem__ not allowed")


        def __iter__(self):
            """
            __iter__
            """

            return self.sorted_keys.__iter__()


        def keys(self):
            """
            Gibt die Namen der Unterknoten zurück

            :rtype: list
            """

            return self.sorted_keys


        def items(self):
            """
            Gibt die Unterknoten-Namen und -Objekte zurück

            :rtype: list
            """

            retlist = []
            for key in self.sorted_keys:
                retlist.append((key, self[key]))
            return retlist


        def iteritems(self):
            """
            Gibt die Unterknoten-Namen und -Objekte zurück
            """

            for key in self.sorted_keys:
                yield (key, self[key])


        def iterkeys(self):
            """
            Gibt die Namen der Unterknoten zurück
            """

            return self.sorted_keys.__iter__()


        def itervalues(self):
            """
            Gibt die Unterknoten-Objekte zurück
            """

            for key in self.sorted_keys:
                yield self[key]


        def values(self):
            """
            Gibt die Unterknoten-Objekte zurück
            """

            retlist = []
            for key in self.sorted_keys:
                retlist.append(self[key])
            return retlist


        def get(self, key, failobj = None):
            """
            Gibt den gewünschten Unterknoten zurück

            :rtype: Node
            """

            return dict.get(self, key, failobj)



    # class SubNodes(object):




    #     def new_item(self, name):
    #         """
    #         Erstellt einen neuen Unterordner im Dateisystem und fügt diesen dem
    #         Dictionary mit den Unterknoten hinzu.
    #
    #         :return: Pfad zum neu erstellten Unterknoten
    #         """
    #
    #         # Name übernehmen, prüfen und Pfad zusammensetzen
    #         name = name.strip()
    #         if not name:
    #             raise EmptyNodeName()
    #         for char in name:
    #             if not char in ALLOWED_NODENAME_CHARS:
    #                 raise NotAllowedCharInNodeName(char)
    #         if name in NOT_ALLOWED_NODENAMES:
    #             raise NotAllowedNodeName(name)
    #         path = os.path.join(self.path, name)
    #
    #         # Prüfen ob der Ordner bereits existiert
    #         if os.path.isdir(path):
    #             raise NodeAlreadyExists(path)
    #
    #         # Prüfen ob der Name als Datei bereits existiert
    #         if os.path.exists(path):
    #             raise FileAlreadyExists(path)
    #
    #         # Ordner erstellen
    #         os.mkdir(path, NEW_DIR_MODE)
    #
    #         # Neuen Ordner einlesen und Schlüssel sortieren
    #         self.subnodes[name] = Node(self, name)
    #         self.sort_keys()
    #
    #         # Fertig
    #         return path


