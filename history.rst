#################
Simple Python CMS
#################


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
