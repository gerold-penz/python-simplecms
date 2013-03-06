#####################################
Installation - Ubuntu ab Version 12.4
#####################################

Ab Ubuntu 12.4 lassen sich die wenigen notwendigen Pakete sehr einfach
installieren. Und Ubuntu-Upstart ist ideal dafür geeignet, eine
"Simple Python CMS"-Instanz mit wenig Aufwand als Dienst laufen zu lassen.


=============
Kurzanleitung
=============

Die benötigten Programmpakete werden mit folgenden Befehlen auf der
Kommandozeile installiert::

  sudo apt-get install python-dev build-essential python-pip python-cherrypy3 python-snappy
  sudo pip install jsonlib2
  sudo pip install Mako
  sudo pip install python-simplecms

Die Details der Installation und die Erstellung einer "Simple Python CMS"-Instanz
werden in den nächsten Kapiteln erklärt.


==========
Python 2.x
==========

Informationen zu Python: http://www.python.org/

Python 2.7 ist bei Ubuntu 12.4 und 12.10 bereits installiert. Es müssen nur noch
die Entwicklerpakete (dev) installiert werden, damit Mako und jsonlib2
(siehe weiter unten) kompiliert werden können.

::

  sudo apt-get install python-dev build-essential


==========
Python-Pip
==========

Informationen zu Pip: https://pypi.python.org/pypi/pip

::

  sudo apt-get install python-pip


========
Jsonlib2
========

Informationen zu Jsonlib2: http://code.google.com/p/jsonlib2/

::

  pip install jsonlib2


=====================
CherryPy Webframework
=====================

Informationen zu CherryPy: http://www.cherrypy.org/

::

  sudo apt-get install python-cherrypy3


=============
Mako Vorlagen
=============

Informationen zu Mako: http://www.makotemplates.org/

Für die Installation von Mako müssen vorher die Pakte `build-essential` und
`python-dev` installiert werden.

::

  sudo pip install Mako


=======================
Snappy Kompressionstool
=======================

Informationen zu Snappy: http://code.google.com/p/snappy/

::

  sudo apt-get install python-snappy


=================
Simple Python CMS
=================

Die Installation von "Simple Python CMS" geht mit `pip` leicht von der Hand.

::

  sudo pip install python-simplecms


=====================================
"Simple Python CMS"-Instanz erstellen
=====================================


=====================
Ubuntu-Upstart-Skript
=====================


====================
Apache Reverse-Proxy
====================

Information über Apache: http://httpd.apache.org/docs/2.2/

Falls bereits Apache als Webserver auf dem Computer eingesetzt wird, kann man
den Apachen dazu verwenden, die Requests der Browser zur
"Simple Python CMS"-Instanz weiterzuleiten. Dazu muss das Apache-Modul
"proxy_http" aktiviert werden.

::

  a2enmod proxy_http


===================
Pound Reverse-Proxy
===================

Informationen über Pound: http://www.apsis.ch/pound







