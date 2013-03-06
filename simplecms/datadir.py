#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import io
import re
import glob
import string
import datetime
import hashlib
import snappy
import isodate
import config
try:
    import jsonlib2 as json
except ImportError:
    import json


# Regeln für neue Nodes bzw. Dateien
NOT_ALLOWED_NODENAMES = {"interface", "_data", "_blobs", "_trash"}
ALLOWED_NODENAME_CHARS = string.ascii_lowercase + string.digits + "_-."
NEW_DIR_MODE = 0770
NEW_FILE_MODE = 0660

# Datentypen
TYPE_UNICODE = "unicode"
TYPE_BOOLEAN = "bool"
TYPE_TIMESTAMP = "timestamp"
TYPE_BLOB_NAME = "blob_name"
#TYPE_INTEGER = "int"
#TYPE_DATE = "date"
#TYPE_TIME = "time"

# Content-Typen mit Textinhalt
TEXT_CONTENT_TYPES = {
    "text/plain",
    "text/html"
}


# ToDo: Blobs mit Snappy komprimiert speichern

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


def find_path(path):
    """
    Gibt den Knoten zurück, der dem übergebenen Pfad entspricht

    :param path: Pfad zum Datenknoten. Dieser muss *immer* mit einem "/"
        beginnen.

    :rtype: Node
    """

    # Parameter
    path = path.strip()
    assert path.startswith("/")
    path = "/" + path.lstrip("/").rstrip("/")

    # Schnelle Rückgabe, falls der gewünschte Knoten bereits eingelesen wurde
    if path in _all_loaded_nodes:
        return _all_loaded_nodes[path]

    # Suche
    current_node = basenode
    for name in path.split("/")[1:]:
        assert isinstance(current_node, Node)
        current_node = current_node.children.get(name)
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
    created_timestamp = None
    modified_timestamp = None
    created_by = None
    modified_by = None
    content_type = None

    # Liste mit den Datenschlüsseln und den zugehörige Datentypen
    # (zusammenpassend mit den Daten-Attributen)
    all_data_keys = [
        {"name": "visible", "type": TYPE_BOOLEAN},
        {"name": "created_timestamp", "type": TYPE_TIMESTAMP},
        {"name": "modified_timestamp", "type": TYPE_TIMESTAMP},
        {"name": "created_by", "type": TYPE_UNICODE},
        {"name": "modified_by", "type": TYPE_UNICODE},
        {"name": "content_type", "type": TYPE_UNICODE},
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
        _content = None # internal
        content_blob_name = None

        # Liste mit den sprachabhängigen Datenschlüsseln
        # (zusammenpassend mit den Daten-Attributen)
        all_data_keys = [
            {"name": "title", "type": TYPE_UNICODE},
            {"name": "menu", "type": TYPE_UNICODE},
            {"name": "description", "type": TYPE_UNICODE},
            {"name": "keywords", "type": TYPE_UNICODE},
            {"name": "content_blob_name", "type": TYPE_BLOB_NAME},
        ]


        def __init__(self, node):
            """
            Init
            """

            self.node = node


        @property
        def content(self):
            """
            Holt den Content aus dem *_content*-Attribut oder aus dem
            *_blobs*-Ordner und gibt diesen entpackt zurück.
            """

            # Falls der Content noch nicht gespeichert wurde, befindet
            # er sich noch in *self._content*.
            if not self._content is None:
                return self._content

            # Nachsehen ob es einen Blob für den Content gibt
            if not self.content_blob_name:
                return None

            # Blob laden, entpacken und zurück geben
            blob_dir = os.path.join(config.DATABLOBSDIR.value, self.content_blob_name[0])
            blob_path = os.path.join(blob_dir, self.content_blob_name)
            with io.open(blob_path, "rb") as blob_file:
                content = snappy.uncompress(blob_file.read())
                if content and self.node.content_type in TEXT_CONTENT_TYPES:
                    return content.decode("utf-8")
                else:
                    return content


        @content.setter
        def content(self, value):
            """
            Speichert den Content unkomprimiert in das *_content*-Attribut
            """

            # Es muss vorher der Content-Type angegeben werden
            if not value is None:
                assert self.node.content_type

            # Zwischenspeichern
            self._content = value

            # Wenn None, dann muss der Blob-Name gelöscht werden
            if value is None:
                self.content_blob_name = None


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

        # Path
        if self.parent:
            self.path = self.parent.path.rstrip("/") + "/" + self.name.rstrip("/")
        else:
            self.path = self.name

        # Klasseninstanz in das globale Dictionary legen
        _all_loaded_nodes[self.path] = self

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
            self[language_id] = self.LangData(self)

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
        for data_key_item in self.all_data_keys:
            data_key_name = data_key_item["name"]
            data_key_type = data_key_item["type"]
            if data_key_type == TYPE_TIMESTAMP:
                timestamp_iso = loaded_data.get(data_key_name, None)
                if timestamp_iso:
                    setattr(self, data_key_name, isodate.parse_datetime(timestamp_iso))
                else:
                    setattr(self, data_key_name, getattr(self, data_key_name))
            else:
                setattr(
                    self,
                    data_key_name,
                    loaded_data.get(data_key_name, getattr(self, data_key_name))
                )

        # Sprachabhängige Daten aus der JSON-Datei zu den
        # sprachabhängigen Klasseninstanzen hinzufügen
        for language_id, language_data in self.items():
            assert isinstance(language_data, self.LangData)

            for data_key_item in language_data.all_data_keys:
                data_key_name = data_key_item["name"]
                data_key_type = data_key_item["type"]
                if data_key_type == TYPE_TIMESTAMP:
                    timestamp_iso = loaded_data.get(
                        data_key_name, {}
                    ).get(
                        language_id, None
                    )
                    if timestamp_iso:
                        setattr(
                            language_data,
                            data_key_name,
                            isodate.parse_datetime(timestamp_iso)
                        )
                    else:
                        setattr(language_data, data_key_name, None)
                else:
                    setattr(
                        language_data,
                        data_key_name,
                        loaded_data.get(data_key_name, {}).get(
                            language_id,
                            getattr(language_data, data_key_name)
                        )
                    )


    def save(self):
        """
        Speichert die Daten ins Dateisystem
        """

        data = {}

        # Timestamp
        now = datetime.datetime.now()
        self.modified_timestamp = now
        if not self.created_timestamp:
            self.created_timestamp = now

        # Datenordner erstellen, falls dieser noch nicht existiert
        if not os.path.isdir(self.datadir_current_path):
            os.makedirs(self.datadir_current_path, NEW_DIR_MODE)

        # Sprachunabhängige Einstellungen ermitteln
        for data_key_item in self.all_data_keys:
            data_key_name = data_key_item["name"]
            data_key_type = data_key_item["type"]
            if data_key_type == TYPE_TIMESTAMP:
                timestamp = getattr(self, data_key_name, None)
                if timestamp:
                    data[data_key_name] = timestamp.isoformat()
                else:
                    data[data_key_name] = None
            else:
                data[data_key_name] = getattr(self, data_key_name, None)

        # Sprachabhängigen *content* in Blob speichern
        for lang in self.keys():

            # Zwischengespeicherten Content ermitteln
            content = self[lang]._content
            if content is None:
                continue

            # Falls es sich um Unicode handelt, wird dieser nach
            # UTF-8 umgewandelt
            if isinstance(content, unicode):
                content = content.encode("utf-8")

            # Blob komprimieren und speichern
            content_compressed = snappy.compress(content)

            # MD5-Hash erstellen und Blob-Namen zusammensetzen
            md5hash = hashlib.md5(content_compressed).hexdigest()
            blob_name = md5hash + ".snappy"
            self[lang].content_blob_name = blob_name

            # Ordner für den Blob erstellen
            blob_dir = os.path.join(config.DATABLOBSDIR.value, blob_name[0])
            if not os.path.isdir(blob_dir):
                os.makedirs(blob_dir, NEW_DIR_MODE)

            # Blob speichern
            blob_path = os.path.join(blob_dir, blob_name)
            if not os.path.isfile(blob_path):
                with io.open(blob_path, "wb") as blob_file:
                    blob_file.write(content_compressed)

            # Temporären Content-Zwischenspeicher löschen
            self[lang]._content = None

        # Sprachabhängige Einstellungen ermitteln
        for data_key_item in self.LangData.all_data_keys:
            data_key_name = data_key_item["name"]
            data_key_type = data_key_item["type"]
            for lang in self.keys():
                if data_key_type == TYPE_TIMESTAMP:
                    timestamp = getattr(self[lang], data_key_name)
                    if timestamp:
                        data.setdefault(
                            data_key_name, {}
                        )[lang] = timestamp.isoformat()
                    else:
                        data.setdefault(
                            data_key_name, {}
                        )[lang] = None
                else:
                    data.setdefault(
                        data_key_name, {}
                    )[lang] = getattr(self[lang], data_key_name)

        # Neuen Namen für JSON-Datei ermitteln
        new_json_filename = now.isoformat() \
            .replace("-", "") \
            .replace(":", "") \
            .replace(".", "")[:17] \
            + ".json"
        new_json_path = os.path.join(self.datadir_current_path, new_json_filename)

        # Neue JSON-Datei speichern
        with io.open(new_json_path, "wb") as new_json_file:
            os.fchmod(new_json_file.fileno(), NEW_FILE_MODE)
            json.dump(data, new_json_file, indent = 2)

        # Alte JSON-Dateien im Current-Ordner mit Snappy komprimieren
        # und in den Archive-Ordner verschieben
        for json_path in glob.glob(
            os.path.join(self.datadir_current_path, "*.json")
        ):
            if json_path == new_json_path:
                continue

            # Archivordner ermitteln und erstellen
            year_str = os.path.basename(json_path)[:4]
            archivedir_path = os.path.join(self.datadir_archive_path, year_str)
            if not os.path.isdir(archivedir_path):
                os.makedirs(archivedir_path, NEW_DIR_MODE)

            # Alte JSON-Datei mit Snappy in den Archivordner komprimieren
            snappy_filename = os.path.basename(json_path) + ".snappy"
            snappy_path = os.path.join(archivedir_path, snappy_filename)

            with io.open(snappy_path, "wb") as snappy_file:
                os.fchmod(snappy_file.fileno(), NEW_FILE_MODE)
                with io.open(json_path, "rb") as old_json_file:
                    snappy_file.write(snappy.compress(old_json_file.read()))

            # Alte JSON-Datei löschen
            os.remove(json_path)


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
        return "<%s '%s'>" % (class_repr, self.path)


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


        def new(self, name):
            """
            Erstellt einen neuen Unterordner im Dateisystem und fügt diesen dem
            Dictionary mit den Unterknoten hinzu.

            :return: Pfad zum neu erstellten Unterknoten
            """

            # Name übernehmen, prüfen und Pfad zum Ordner zusammensetzen
            name = name.strip()
            if not name:
                raise EmptyNodeName()
            for char in name:
                if not char in ALLOWED_NODENAME_CHARS:
                    raise NotAllowedCharInNodeName(char)
            if name in NOT_ALLOWED_NODENAMES:
                raise NotAllowedNodeName(name)
            nodedir_path = os.path.join(self.parent.nodedir_path, name)

            # Prüfen ob der Ordner bereits existiert
            if os.path.isdir(nodedir_path):
                raise NodeAlreadyExists(nodedir_path)

            # Prüfen ob der Name als Datei bereits existiert
            if os.path.exists(nodedir_path):
                raise FileAlreadyExists(nodedir_path)

            # Ordner erstellen
            os.mkdir(nodedir_path, NEW_DIR_MODE)

            # Neuen Ordner einlesen und Schlüssel sortieren
            new_node = Node(self.parent, name)
            dict.__setitem__(self, name, new_node)
            self.sort_keys()

            # Daten speichern
            new_node.save()

            # Fertig
            return nodedir_path

