#################
Simple Python CMS
#################

**Content Management System - Made Simple**

Mein Ziel ist es, ein Content Management System (CMS) zu programmieren,
das möglichst einfach (zumindest in meinen Augen) bedienbar ist.
Bitte nicht falsch verstehen: Es ist nicht Teil des Ziels, ein einfach zu
installierendes CMS zu erstellen. Die Installation hat es in sich.
Das Ergebnis wird aber ein sehr einfach bedienbares CMS sein.


**Das Projekt befindet sich momentan in der Planungsphase.**


=======
Technik
=======

Als begeisterter Python_-Programmierer, der kleine und feine Tools schätzt,
werde ich als Web-Framework CherryPy_ einsetzen.
Als Vorlagensprache habe ich mich für Mako_ entschieden.

.. _Python: http://www.python.org/
.. _CherryPy: http://www.cherrypy.org/
.. _Mako: http://www.makotemplates.org/

Das Datenbanksystem ist noch nicht entschieden...


========
Features
========

Das sind die Features die ich mir von *Simple Python CMS* erwarte.


-----------------------
Einfache Berechtigungen
-----------------------

- Nicht angemeldet

  - Darf die Website sehen

- Angemeldet

  - Darf (vielleicht) Kommentare abgeben

- Admin

  - Darf die Site verändern


----------
Rückgängig
----------

Änderungen an einer Seite können rückgängig gemacht werden. Wie in einem Wiki
soll es eine Auflistung der Änderungen geben. Und man soll jede Version
wiederherstellen können.

Eine wiederhergestellte Version wird als neue Version gespeichert, so dass man
die Wiederherstellung selbst auch rückgängig machen kann.


-----------------------
Einfach Seite erstellen
-----------------------

Folgt ein Admin einem Link zu einer nicht existierenden Seite, dann wird eine
Seite angezeigt, die es dem Admin ermöglicht die fehlende Seite zu erstellen.


------------------------------------------
Bilder und Dateien hochladen und verwalten
------------------------------------------


--------------------------------
Vorlagen für die gesamte Website
--------------------------------

Mehrere Vorlagen sind möglich.
Es handelt sich dabei um *globale Vorlagen* die für das Layout der gesamten
Seite zuständig ist. Mehrere Spalten, Header und Footer möglich.

Einige Vorlagen werden gleich mit *Simple Python CMS* ausgeliefert.

Ich gehe vorerst mal davon aus, dass *Simple Python CMS* mit YAML_-Vorlagen
umgehen können soll.

.. _YAML: http://www.yaml.de/

Die Standard-Vorlage wird einstellbar sein.

Jede Seite kann die Standard-Vorlage oder eine andere Vorlage als
*globale Vorlage* verwenden. Einfach per Combobox einstellbar.


------------------------
Vorlagen für den Content
------------------------

- Einspaltig

- Zweispaltig

Ob und wie ich das umsetzen werde, weiß ich noch nicht.


------------
Mehrsprachig
------------

Gleich von Beginn an soll auf Mehrsprachigen Content geachtet werden.

Der Text der im CMS anfällt, wird mit Gettext übersetzt. Jede Seite wird
mehrsprachig abgespeichert.

Es wird eine Einstellung geben, die festlegt welche Sprachen im CMS möglich sind.


---------
Hauptmenü
---------

Das Hauptmenü ist eine UL-LI-Kombination, die automatisch aus der
Verzeichnissstruktur erstellt wird.

Jeder Ordner hat Metadaten, die bestimmen, ob ein Ordner im Hauptmenü
ein- oder auszublenden ist. Die Ordner bekommen die Übersetzungen für
das Hauptmenü gleich mitgeliefert.

Das Hauptmenü (die UL-LI-Kombination) kann als Textmakro überall in der
globalen Vorlage eingebunden werden.


-------------
Planungsphase
-------------

Es geht noch weiter ...


======
Inhalt
======

.. toctree::
   :maxdepth: 1

   installation/index.rst



.. ==================
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
