#################
Simple Python CMS
#################


==============
Version 0.1.10
==============

2013-03-30

- *setup.py* leicht angepasst.


=============
Version 0.1.9
=============

2013-03-24

- Es können jetzt auch fünfstellige Sprachkürzel zusätzlich zu den zweistelligen
  Sprachkürzeln verwendet werden. Z.B. ``["de", "de_AT", "de_DE"]``

- ``node["auto"]`` gibt jetzt das *LangDataAuto*-Objekt zurück, das sich
  automatisch um die Spracherkennung kümmert und alle bevorzugten Sprachen in
  der vom Browser gewünschten Reihenfolge durchläuft und die Attribute des
  *LangData*-Objektes in der best möglichen Sprache zurück gibt.


=============
Version 0.1.8
=============

2013-03-23

- Beim Auslesen des Contents aus dem Blob-Ordner werden nur Dateien mit Snappy
  dekomprimiert, die die Dateiendung ".snappy" haben.

- Set mit nicht gut komprimierbaren Mime-Typen zusammengestellt:
  *constants.CONTENT_TYPES_NOT_COMPRESSIBLE*

- Beim Speichern des Contents in den Blob-Ordner, werden nur diese Dateien
  mit Snappy komprimiert, deren Mime-Type nicht im Set
  *constants.CONTENT_TYPES_NOT_COMPRESSIBLE* enthalten ist.

- Das neue Modul *language.py* ist für Sprachermittlung und Übersetzungen
  zuständig.

- Das neue Modul *cookie.py* ist für das Lesen und Schreiben von Cookies
  zuständig.


=============
Version 0.1.7
=============

2013-03-06

- Beschreibung des *Datadir*-Systems in die Dokumentation geschrieben.

- Beim Lesen und Schreiben der Daten aus den JSON-Dateien werden jetzt die
  Datentypen berücksichtigt. Primär geht es hier um "timestamp" als Datentyp,
  der beim Schreiben in die JSON-Datei nach ISO um gewandelt wird. Beim Lesen
  wird der ISO-String nach *datetime.datetime* umgewandelt.

- Hinzufügen eines neuen Nodes

- Das *content*-Attribut von *datadir.Node.LangData* wird jetzt als
  komprimierter Blob gespeichert.
  Bei jeder Anforderung von *content* wird der Blob aus dem Dateisystem
  ausgelesen, dekomprimiert und zurück gegeben.
  *content* bleibt also nicht im Speicher, da *content* beliebig groß sein
  kann.


=============
Version 0.1.6
=============

2013-03-05

- *datadir.get_url* nach *datadir.get_path* umbenannt

- *datadir*: jedes Vorkommen von *url* nach *path* umbenannt.

- Speichern der Daten eines Nodes in das Dateisystem.
  Die Daten werden in JSON-Dateien gespeichert. Nach dem Speichern werden
  alte JSON-Dateien, die sich noch im "current"-Ordner befinden, mit Snappy 
  komprimiert und in den "archive"-Ordner verschoben. 
  Die alten JSON-Dateien werden danach gelöscht.


=============
Version 0.1.5
=============

2013-03-03

- *datadir.Node* um *children* erweitert. Somit ist es jetzt möglich, vom 
  Knoten aus die Unterknoten abzufragen.

- Die Funktion *datadir.get_url* gibt den Knoten zurück dem die URL entspricht.
  Damit kann man sehr schnell einen Knoten auswählen.


=============
Version 0.1.4
=============

2013-03-02

- Die beste Struktur des Datenordners durch Versuche herausgefunden.

- Die beste *datadir*-Objektstruktur herausgefunden

- Weitere Tests mit verschieden aufgebauten Datenstrukturen


=============
Version 0.1.3
=============

2013-02-25

- Struktur etwas angepasst. *lib*-Ordner wurde entfernt. Die Module des
  *lib*-Ordners sind jetzt direkt im *simplecms*-Ordner zu finden.

- *Folder*-Objekte sind jetzt *Node*-Objekte. Das liegt daran, dass ich
  entschieden habe, dass jede Seite ein *Node* ist und und jede Unterseite
  auch wieder ein *Node*. Die Metadaten werden direkt an das Node-Objekt
  gebunden, was bei *Folder* als Name etwas merkwürdig erscheinen würde.

- Installationsanleitung ergänzt

- Fehlerklassen im *datadir*-Modul umbenannt

- Beim Initialisieren eines Nodes werden gleich auch die Metadaten des Nodes
  geladen und an die Node-Instanz gebunden. Z.B. "title", "visible", ...

- Für das Parsen der JSON-Dateien ist standardmäßig *jsonlib2* zuständig.
  Kann *jsonlib2* nicht gefunden werden, übernimmt das Standardmodul *json*
  die Arbeit.

- Tests mit *Property* für die Metadaten


=============
Version 0.1.2
=============

2013-02-22

- Weitere Anpassungen von *lib.datadir*

- Erstellen eines Unterordners im Datenordner und zugehörige Tests

- Kleine Nachbearbeitungen von *lib.datadir*


=============
Version 0.1.1
=============

2013-02-22

- Die Grundüberlegungen zur Struktur sind abgeschlossen.

- Mit der Datenordner-Verwaltung begonnen. Die meisten Änderungen befinden sich
  in *lib.datadir*. Über *lib.datadir.tree* kann auf den kompletten
  DATATREEDIR zugegriffen werden.


=============
Version 0.0.7
=============

2013-02-21

Die James Bond-Version :-)

- Mit den Einstellungen Tests durchgeführt

- *lib.config* ist der direkte Zugang zu *cherrypy.config*. Zusätzlich werden
  die Konfigurationen beschrieben. Das dient später dem Erstellen der 
  Dokumentation der Konfiguration einer CMS-Instanz.

- Minimale *http_root*-Ordnerstruktur (css, js, interface) erstellt.

- Beim Starten der Anwendung werden die Datenordner erstellt, falls diese
  noch nicht existieren.

- *lib.constants* um die Konstante HTTPROOTDIR erweitert

- Die Konfigurationen DATAJSDIR, DATACSSDIR und DATATREEDIR werden beim
  ersten schreiben der Konfiguration DATADIR automatisch eingestellt.


=============
Version 0.0.6
=============

2013-02-20

- Dokumentation
    
    - Als Datenbank wird Redis eingesetzt
    
    - Angefangen, die Installation zu beschreiben

- Mako-Tests


=============
Version 0.0.5
=============

2013-02-19

- Gedanken über die Datenbank gemacht.

- Versuche, Redis als eingebundene Datenbank zu verwenden. Vielleicht kann
  man Redis als "Embedded Database" verwenden.

- *googlecode_upload* eingebunden. Damit können Dateien direkt zu Google-Code
  hochgeladen werden.

- Das Programm *_setup_upload.py* läd das vorher mit *_setup_sdist.py* gepackte
  Quellcode-Archiv automatisch zu Google-Code hoch.

- Tests mit Redis als Datenbankserver. Es sieht gut aus. Redis lässt sich unter 
  Linux ziemlich gut verwenden. Tests mit Windows mache ich später einmal.


=============
Version 0.0.4
=============

2013-02-19

- Dokumentation

  - Featureliste erweitert

  - Technik-Seite erstellt und Gedanken über die zu verwendende Technik gemacht


=============
Version 0.0.3
=============

2013-02-19

- an Dokumentation gearbeitet

- Featureliste geschrieben


=============
Version 0.0.2
=============

2013-02-18

- *_sphinx_make_html.py* kopiert jetzt die erstellte Sphinx-Dokumentation
  automatisch in den *python-simplecms-gh-pages*-Ordner.


=============
Version 0.0.1
=============

2013-02-16

- Erstimport
