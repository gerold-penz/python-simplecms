########
Features
########


.. index::
  Wiki
  Ordnerstruktur

====================
Ähnlich wie ein Wiki
====================

Das CMS soll teilweise wie ein Wiki funktionieren. Verlinkt man auf eine
nicht existierende Seite, kann man diese Seite erstellen und sofort mit
dem Befüllen beginnen. Es soll aber eine Ordnerstruktur geben, die als
Menüstruktur abgebildet wird. Ob ein Ordner im Menü auftauchen soll, kann
eingestellt werden.

.. index::
  History

Änderungen sollen alle gespeichert werden, so dass man zu jedem
beliebigen Stand einer Seite zurückkehren kann. Wie in einem Wiki
soll es eine Auflistung der Änderungen geben. Und man soll jede Version
wiederherstellen können.

Eine wiederhergestellte Version wird als neue Version gespeichert, so dass man
die Wiederherstellung selbst auch rückgängig machen kann.


.. index::
  Markdown
  MediaWiki
  reStructuredText
  rest
  rst
  WYSIWYG-Editor
  TinyMCE
  Markupsprache

============================
Mehrere Eingabemöglichkeiten
============================

Texte sollen in mehreren Markup-Sprachen (z.B. *reStructuredText*,
*Markdown*, *MediaWiki*, ...), oder mit einem WYSIWYG-Editor (z.B. TinyMCE)
eingegeben oder geändert werden können.

Nachteil: Hat man sich bei einer Seite einmal für eine Markupsprache
entschieden, kann das nicht mehr geändert werden.


.. index::
  Vorlage
  Textmakro
  Layout
  Tabellenlayout
  Spalten
  Seitenvorlage
  YAML

=======================
Vorlagen und Textmakros
=======================

Mit Hilfe von **Textmakros** soll jede beliebige andere CMS-Seite in eine
Seite importiert werden können. So dass man Teile einer Seite an
verschiedenen Stellen editieren kann. So kann z.B. ein Tabellenlayout mit
drei Spalten aufgebaut werden.

Seitenvorlagen beziehungsweise Layouts sollen für jede Seite
auswählbar sein. Z.B. "Einspaltig", "Zwei Spalten", "Drei Spalten". Bei so
einem Dreispaltenlayout könnte der Inhalt der äußeren Spalten von zwei
anderen Seiten kommen und der Inhalt der mittleren Spalte kommt von der
Seite selbst.

Mehrere Vorlagen sind auswählbar. *Seitenvorlagen* sind für das Layout der
gesamten Seite zuständig. Einige Vorlagen werden gleich mit *Simple Python CMS*
ausgeliefert.

Jede Seite kann die Standard-Vorlage oder eine andere Vorlage als
*Seitenvorlage* verwenden. Einfach per Combobox einstellbar.

Ich gehe vorerst mal davon aus, dass *Simple Python CMS* mit YAML_-Vorlagen
umgehen können soll.

.. _YAML: http://www.yaml.de/

Die Standard-Vorlage wird einstellbar sein.


.. index::
  Berechtigungssystem
  Admin
  Anmeldung
  Kommentar
  Schreibzugriff

=======================
Einfache Berechtigungen
=======================

Da alles *einfach* sein soll, werde ich nur ein
**einfaches Berechtigungssystem** programmieren. Es gibt **nicht angemeldet**,
**angemeldet** und **Admin**. Nicht am CMS angemeldete Personen dürfen nur
lesen. Angemeldete Personen dürfen Kommentare schreiben und Admins haben
vollen Schreibzugriff.


.. index::
  Bilder
  Dateien
  hochladen
  Ordnerstruktur
  WYSIWYG-Editor
  Link zu Bildern
  Link zu Dateien

==========================================
Bilder und Dateien hochladen und verwalten
==========================================

Bilder können überall in der gesamten Ordnerstruktur des CMS abgespeichert
werden. Dafür wird eine Bild- und Dateiverwaltung geschrieben.

Wird ein Bild über den WYSIWYG-Editor hochgeladen, landet das Bild im
selben Ordner in dem sich auch die Seite befindet

Das Hochladen von Bildern in einen Ordner soll in allen Editoren möglich sein.
Je nach Markup-Sprache wird es eine Möglichkeit geben, ein Bild hochzuladen
und den Link dazu sofort in den Text der Seite einzubetten.


.. index::
  Content
  Sprache
  Cookie
  Babel
  Übersetzung

============
Mehrsprachig
============

Gleich von Beginn an soll auf mehrsprachigen Content geachtet werden.

Automatische Erkennung der Browser-Sprache. Wurde eine Sprache ausgewählt,
wird diese per Cookie fixiert.

Der Stammtext des Programmes selbst, wird mit Babel_ übersetzt.
Jede Content-Seite wird von Anfang an in mehreren Sprachen abgespeichert.

.. _Babel: http://babel.edgewall.org/

Es wird eine Einstellung geben, die festlegt welche Sprachen im CMS möglich sind.


.. index::
  Menü
  Verzeichnisstruktur
  Metadaten
  Übersetzung
  Textmakro

=========
Hauptmenü
=========

Das Hauptmenü ist eine UL-LI-Kombination, die automatisch aus der
Verzeichnisstruktur erstellt wird.

Jeder Ordner hat Metadaten, die bestimmen, ob ein Ordner im Hauptmenü
ein- oder auszublenden ist. Die Ordner bekommen die Übersetzungen für
das Hauptmenü gleich mitgeliefert.

Das Hauptmenü (die UL-LI-Kombination) kann als Textmakro überall in die
Seitenvorlagen eingebunden werden.


