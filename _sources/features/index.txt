########
Features
########

====================
Ähnlich wie ein Wiki
====================

Das CMS soll teilweise wie ein Wiki funktionieren. Verlinkt man auf eine
nicht existierende Seite, kann man diese Seite erstellen und sofort mit
dem Befüllen beginnen. Es soll aber eine Ordnerstruktur geben, die als
Menüstruktur abgebildet wird. Ob ein Ordner im Menü auftauchen soll, kann
eingestellt werden.

Änderungen sollen alle gespeichert werden, so dass man zu jedem
beliebigen Stand einer Seite zurückkehren kann. Wie in einem Wiki
soll es eine Auflistung der Änderungen geben. Und man soll jede Version
wiederherstellen können.

Eine wiederhergestellte Version wird als neue Version gespeichert, so dass man
die Wiederherstellung selbst auch rückgängig machen kann.

Folgt man einem Link zu einer nicht existierenden Seite, dann wird eine
Seite angezeigt, die es ermöglicht die fehlende Seite zu erstellen.


============================
Mehrere Eingabemöglichkeiten
============================

Texte sollen in mehreren Markup-Sprachen (z.B. *reStructuredText*,
*Markdown*, *MediaWiki*, ...), oder mit einem WYSIWYG-Editor (z.B. TinyMCE)
eingegeben oder geändert werden können.


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


=======================
Einfache Berechtigungen
=======================

Da alles *einfach* sein soll, werde ich nur ein
**einfaches Berechtigungssystem** programmieren. Es gibt **nicht angemeldet**,
**angemeldet** und **Admin**. Nicht am CMS angemeldete Personen dürfen nur
lesen. Angemeldete Personen dürfen Kommentare schreiben und Admins haben
vollen Schreibzugriff.


==========================================
Bilder und Dateien hochladen und verwalten
==========================================


================================
Vorlagen für die gesamte Website
================================


============
Mehrsprachig
============

Gleich von Beginn an soll auf Mehrsprachigen Content geachtet werden.

Der Text der im CMS anfällt, wird mit Gettext übersetzt. Jede Seite wird
mehrsprachig abgespeichert.

Es wird eine Einstellung geben, die festlegt welche Sprachen im CMS möglich sind.


=========
Hauptmenü
=========

Das Hauptmenü ist eine UL-LI-Kombination, die automatisch aus der
Verzeichnissstruktur erstellt wird.

Jeder Ordner hat Metadaten, die bestimmen, ob ein Ordner im Hauptmenü
ein- oder auszublenden ist. Die Ordner bekommen die Übersetzungen für
das Hauptmenü gleich mitgeliefert.

Das Hauptmenü (die UL-LI-Kombination) kann als Textmakro überall in der
globalen Vorlage eingebunden werden.


=============
Planungsphase
=============

Es geht noch weiter ...

