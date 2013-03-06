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

Da sich Mako_ sehr ähnlich wie CheetahTemplate anfühlt, aber auch mit
Python 3.x funktioniert, habe ich mich für Mako entschieden. Weiters kommt dazu,
dass Mako ausgeklügelte Caching-Mechanismen anbietet und Mako-Vorlagen nicht wie
ein *Klammerngewitter* ({{ }}) ;-) aussehen.
Ich mag es, dass Mako *nicht versucht*, die Möglichkeiten von Python zu
beschneiden. Andere Vorlagensprachen tun ja alles um komplett anders als die
gewohnte Programmiersprache auszusehen. Was aber ein einfaches Zusammensetzen
und mehrmaliges Verwenden von Variablen innerhalb der Vorlage meist unterbindet.
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
erstellte Struktur direkt in das CMS einbinden kann. Unbedingt ausprobieren.


.. index::
  Datenbank
  SQLite
  CouchDB
  Redis

===============
Datenbanksystem
===============

----------------------------------------
Überlegungen die wieder verworfen wurden
----------------------------------------

Eigentlich bräuchte ich so etwas schnelles wie Redis_, einen einfachen
Dokumentenspeicher wie CouchDB_ und eine einfach einzubauende Datenbank
wie SQLite_.

Für Redis und CouchDB müssen TCP-Ports geöffnet werden. Redis lässt sich unter
Linux einfach installieren und ist superschnell. Wenn aber mehrere
"Simple Python CMS" auf einem System betrieben werden sollen,
muss man sich eine gute Trennung zwischen den einzelnen Datenbanken
überlegen oder man lässt Redis für jede "Simple Python CMS"-Instanz
als eigenständiges Programm laufen.
Dann ist aber noch zu bedenken, dass einzelne Instanzen gezielt gestartet
und gestoppt werden müssen. Was wieder einen erhöhten Aufwand beim
Installieren bringt, den nicht jeder schaffen wird. Ähnliches gilt für
CouchDB. Eigener TCP-Port. Mehrere Instanzen nur umständlich.

SQLite ist ein "Relationales Datenbanksystem", das die Daten in nur *einer*
Datei hält. Mehrere Programme/Prozesse können gleichzeitig lesend auf die
Datenbankdatei zugreifen.
Beim Schreiben wird die Datenbank kurzfristig für die anderen zugreifenden
Programme gesperrt.
Damit kann man bei kleinen bis mittleren Content Management Systemen
sicher gut leben.

Bei CouchDB ist es problemlos möglich, weitere Datenfelder im Laufe der
Entwicklung zu den Datenbank-Dokumenten hinzuzufügen, ohne dass man etwas
an der Struktur der Datenbank ändern muss. Dafür ist die Abfrage der Daten
nicht so einfach wie bei Redis oder SQLite.

Redis bietet vielfältige Möglichkeiten und interessante Datenstrukturen an um
die Daten zu speichern und schnell wieder zu finden.
Noch dazu ist Redis wirklich schnell und lässt sich von Python aus wunderbar
einfach programmieren. Wie bei CouchDB lassen sich problemlos weitere
Datenfelder im Laufe der Entwicklung hinzufügen, ohne die Datenbank-Strukturen
aller "Simple Python CMS"-Instanzen ständig aktuell halten zu müssen. Diese
aktualisieren sich sozusagen von selbst, wenn man nicht zu chaotisch programmiert.

Mal sehen, ob ich eine Möglichkeit finde, Redis zu verwenden...

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Überlegungen, wie Redis verwendet werden könnte
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Redis wird per `subprocess.Popen` in einem eigenen Thread gestartet. Statt
einer TCP-Verbindung wird die Kommunikation per Unix-Socket aufgebaut. Das ist
schneller als TCP und bietet eine einfache Möglichkeit, für jede
"Simple Python CMS"-Instanz einen eigenen Socket im Datenbankordner der
Instanz zu öffnen.

Da es von jeder "Simple Python CMS"-Instanz normalerweise nur *einen Prozess*
gibt, wird Redis nur einmal je "Simple Python CMS"-Instanz gestartet.
Ich werde aber die Möglichkeit offen halten, dass Redis als eigenständiger
Server läuft und eine "Simple Python CMS"-Instanz mehrmals
gestartet werden kann. Das bedeutet aber mehr Aufwand für den Admin
und soll nicht der Normalfall werden.


-----
Fazit
-----

Nach vielen, vielen Stunden in denen ich über die perfekte Datenbanklösung
nachgedacht habe -- bin ich zu dem Schluss gekommen,
die Daten in das Dateisystem und nicht in eine Datenbank zu schreiben.


=======
Datadir
=======

Anstatt die Daten alle in eine Datenbank zu schreiben, habe ich mich dazu
entschlossen, diese direkt in das Dateisystem zu schreiben. Jede CMS-Seite
bekommt einen eigenen Ordner im Dateisystem. Die Einstellungen einer Seite
werden als JSON-Datei im jeweiligen *_data/current*-Ordner abgelegt.
Ändert man eine Einstellung, wird eine neue JSON-Datei im
*_data/current*-Ordner erstellt. Die alte JSON-Datei wird komprimiert in dem
*_data/archive*-Ordner abgelegt.
Mit diesem System kann ich jede Änderung wieder rückgängig machen.

Beim Starten des Content Management Systems wird ein Datenordner bestimmt.
In diesem Datenordner werden alle Daten des CMS abgelegt. Es wird einen
eigenen Ordner für die Binärdaten geben. Dieser befindet sich direkt im
Daten-Hauptordner und heißt *_blobs*.

In den JSON-Dateien werden nur die Einstellungen einer Seite oder eines
Bildes abgelegt. Der Content selbst, also der HTML-Text oder die Bilddaten
werden im *_blobs*-Ordner abgelegt. Bevor die Datei in den *_blobs*-Ordner
gespeichert wird, wird diese mit *Snappy* komprimiert und ein MD5-Hash
generiert, der den Inhalt der Blob-Datei eindeutig kennzeichnet. Der MD5-Hash
wird dann der Name der Blob-Datei. Ziel ist es, keine Daten doppelt
abzuspeichern.

Dateien die mit Snappy komprimiert werden, bekommen als zusätzliche
Dateiendung ".snappy" hinzugefügt.

Es gibt einen Ordner mit dem Namen *_trash*, der sich direkt im Datenordner
befindet. Dort werden alle gelöschten Elemente abgelegt. Somit können auch
gesamte, gelöschte Ordner inklusive aller darin enthaltenen Unterordner
wiederhergestellt werden. Die Blobs verbleiben im *_blobs*-Ordner, bis es
keine Referenz mehr darauf gibt.

Zusammenfassend: Jede CMS-Seite und jeder sonstige Inhalt des CM-Systems wird
im Datenordner abgespeichert. Jedes Objekt, egal ob es sich um eine HTML-Seite
oder um ein Bild handelt, wird durch einen **Ordner** unterhalb des
Datenordners repräsentiert. Jeder Ordner im Datenordner kann natürlich auch
Unterordner enthalten. Das bedeutet, dass sogar Bilder einen Unterordner
haben können. Das kann z.B. dazu verwendet werden, verkleinerte Bilder
(Thumbnails) unterhalb des Hauptbildes abzuspeichern. Das hochgeladene
Bild könnte z.B. diesen Pfad haben: "/images/banner01.jpg". Und das zugehörige
Thumbnail könnte z.B. diesen Pfad haben: "/images/banner01.jpg/thumbnail".
Ob man das so verwendet oder nicht, steht jedem frei.












.. _Python: http://www.python.org/
.. _CherryPy: http://www.cherrypy.org/
.. _CheetahTemplate: http://www.cheetahtemplate.org/
.. _Mako: http://www.makotemplates.org/
.. _YAML: http://www.yaml.de/
.. _Thinkintags: http://www.thinkintags.com/
.. _Redis: http://redis.io/
.. _CouchDB: http://couchdb.apache.org/
.. _SQLite: http://www.sqlite.org/









