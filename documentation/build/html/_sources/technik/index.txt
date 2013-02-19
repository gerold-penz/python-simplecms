#######
Technik
#######

.. index::
  Python

==================
Programmiersprache
==================

Python_, die schönste Programmiersprache der Welt, natürlich, was sonst? ;-)


.. index::
  Python
  Webframework
  CherryPy

=============
Web-Framework
=============

Als begeisterter Python_-Programmierer, der kleine und feine Tools schätzt,
werde ich als Web-Framework CherryPy_ einsetzen.

Damit habe ich in den letzen paar Jahren viel Erfahrung sammeln können.
Ich bin so sehr mit CherryPy zufrieden, dass kein anderes Web-Framework in
Frage kommt.


.. index::
  Vorlage
  CheetahTemplate
  Mako
  Python

===============
Vorlagensprache
===============

Den Schritt zu Python 3.x möchte ich mir nicht versperren.
Deshalb werde ich diesmal nicht mehr auf CheetahTemplate_ zurückgreifen.
Es ist zwar schade, denn CheetahTemplate bietet mir die volle Flexibilität
von Python, ohne kompliziert zu wirken, was ich sehr schätze.

Da sich Mako_ sehr ähnlich wie CheetahTemplate anfühlt, aber auch mit Python 3.x
funktioniert, habe ich mich für Mako entschieden. Weiters kommt dazu, dass
Mako ausgeklügelte Caching-Mechanismen anbietet und Mako-Vorlagen nicht wie
ein *Klammerngewitter* ({{ }}) ;-) aussehen.
Ich mag es, dass Mako *nicht versucht*, die Möglichkeiten von Python zu beschneiden.
Andere Vorlagensprachen tun ja alles um komplett anders als die gewohnte
Programmiersprache auszusehen. Was aber ein einfaches Zusammensetzen und
mehrmaliges Verwenden von Variablen innerhalb der Vorlage meist unterbindet.
So müsste man jede *Kleinigkeit* in den Programmcode verlagern, was ich nicht
immer für die beste Lösung halte.


.. index::
  YAML
  Thingintags
  Textmakro
  HTML

=============
CSS Framework
=============

YAML_ scheint für meine Zwecke ideal, da sich jeder selbst sein Layout
damit gestalten kann. Und Platzhalter/Textmakros zeigen die Stellen an,
die dynamisch mit Content befüllt werden sollen.
Die Dokumentation zu YAML ist hervorragend.
Ich habe noch keine Erfahrung mit YAML, aber ausprobieren werde ich es sicher.

Mit Thinkintags_ gibt es ein aufstrebendes Werkzeug um HTML-Seiten
zu designen. Vielleicht bringe ich es so hin, dass man die damit
erstellte Struktur direkt in das CMS einbinden kann.


.. index::
  Datenbank
  SQLite

===============
Datenbanksystem
===============

Das Datenbanksystem ist noch nicht entschieden...

Eigentlich bräuchte ich so etwas Schnelles wie Redis_, einen einfachen
Dokumentenspeicher wie CouchDB_ und so etwas einfach zu verwendendes
wie SQLite_.

Für Redis und CouchDB müssen TCP-Ports geöffnet werden. Redis lässt sich
einfach installieren und ist superschnell. Wenn aber mehrere "Simple Python CMS"
auf einem System betrieben werden sollen, muss man sich eine gute Trennung
zwischen den einzelnen Datenbanken überlegen oder man lässt Redis für jede
"Simple Python CMS"-Instanz als eigenständiges Programm laufen. Dann ist aber
noch zu bedenken, dass einzelne Instanzen gezielt gestartet und gestoppt werden
müssen. Was wieder einen erhöhten Aufwand beim Installieren bringt, den nicht
jeder schaffen wird. Ähnliches gilt für CouchDB. Eigener TCP-Port.
Mehrere Instanzen nur umständlich.

SQLite ist ein "Relationales Datenbanksystem", das die Daten in *einer* Datei
hält. Mehrere Programme können gleichzeitig lesend auf die Datenbankdatei
zugreifen. Beim Schreiben wird die Datenbank kurzfristig für die anderen
zugreifenden Programme gesperrt.
Damit kann man bei kleinen bis mittleren Content Management Systemen
sicher gut leben.

Bei CouchDB ist es problemlos möglich, weitere Datenfelder im Laufe der
Entwicklung zu den Datenbank-Dokumenten hinzuzufügen, ohne dass man etwas
an der Struktur der Datenbank ändern muss. Dafür ist die Abfrage der Daten
nicht so einfach wie bei Redis oder SQLite.

Redis bietet viele Möglichkeiten beziehungsweise Strukturen an um die
Daten zu speichern und wieder zu finden. Noch dazu ist Redis wirklich schnell
und lässt sich von Python aus wunderbar einfach programmieren.

Mal sehen, ob ich eine Möglichkeit finde, Redis trotzdem zu verwenden.






.. _Python: http://www.python.org/
.. _CherryPy: http://www.cherrypy.org/
.. _CheetahTemplate: http://www.cheetahtemplate.org/
.. _Mako: http://www.makotemplates.org/
.. _YAML: http://www.yaml.de/
.. _Thinkintags: http://www.thinkintags.com/
.. _Redis: http://redis.io/
.. _CouchDB: http://couchdb.apache.org/
.. _SQLite: http://www.sqlite.org/









