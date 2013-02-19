#################
Simple Python CMS
#################

**Content Management System - Made Simple**

Mit **Simple Python CMS** möchte ich ein einfach einzusetzendes
Content Management System (CMS) auf Basis von Python und CherryPy
erstellen, das ich für meine private Homepage verwenden kann.

Mein Ziel ist es, ein Content Management System zu programmieren,
das möglichst einfach (zumindest in meinen Augen) bedienbar ist.

Bitte nicht falsch verstehen: Es ist nicht Teil des Ziels, ein einfach zu
installierendes CMS zu erstellen. Die Installation hat es in sich.
Das Ergebnis wird aber ein sehr einfach bedienbares CMS sein.

Das CMS soll teilweise wie ein Wiki funktionieren. Verlinkt man auf eine
nicht existierende Seite, kann man diese Seite erstellen und sofort mit
dem Befüllen beginnen. Es soll aber eine Ordnerstruktur geben, die als
Menüstruktur abgebildet wird. Ob ein Ordner im Menü auftauchen soll, kann
eingestellt werden.

Texte sollen in mehreren Markup-Sprachen (z.B. *reStructuredText*,
*Markdown*, *MediaWiki*, ...), oder mit einem WYSIWYG-Editor (z.B. TinyMCE)
eingegeben oder geändert werden können.

Mit Hilfe von **Textmakros** soll jede beliebige andere CMS-Seite in eine
Seite importiert werden können. So dass man Teile einer Seite an
verschiedenen Stellen editieren kann. So kann z.B. ein Tabellenlayout mit
drei Spalten aufgebaut werden.

Seitenvorlagen beziehungsweise Seitenstrukturen sollen für jede Seite
auswählbar sein. Z.B. "Einspaltig", "Zwei Spalten", "Drei Spalten". Bei so
einem Dreispaltenlayout könnte der Inhalt der äußeren Spalten von zwei
anderen Seiten kommen und der Inhalt der mittleren Spalte kommt von der
Seite selbst.

Anleihe aus den WIKIs: Änderungen sollen alle gespeichert werden, so dass
man zu jedem beliebigen Stand einer Seite zurückkehren kann.

Da alles *einfach* sein soll, werde ich nur ein **einfaches
Berechtigungssystem** programmieren. Es gibt **nicht angemeldet**,
**angemeldet** und **Admin**. Nicht am CMS angemeldete Personen dürfen nur
lesen. Angemeldete Personen dürfen Kommentare schreiben und Admins haben
vollen Schreibzugriff.


======
Status
======

Das Projekt befindet sich momentan in der Planungsphase.


======
Inhalt
======

.. toctree::
   :maxdepth: 1

   features/index.rst
   technik/index.rst
   installation/index.rst



.. ==================
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
