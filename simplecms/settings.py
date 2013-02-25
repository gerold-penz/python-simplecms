#!/usr/bin/env python
# coding: utf-8
"""
Einstellungen

Über dieses Modul werden alle Einstellungen des Programmes verwaltet

Created 2013-02-21 by Gerold - http://halvar.at/
"""


# # Alle Einstellungen in einem globalen Dictionary
# _global_all_settings = {}
#
#
# class Setting(object):
#     """
#     Repräsentiert eine Einstellung
#     """
#
#     DATASOURCE_MEMORY = 1
#
#
#     def __init__(
#         self,
#         name,
#         datasources,
#         short_description,
#         long_description = None,
#         default = None
#     ):
#
#         global _global_all_settings
#
#         self.name = unicode(name)
#         self.datasources = datasources
#         self.short_description = unicode(short_description)
#         self.long_description = unicode(long_description) if long_description else None
#         self.default = default
#
#         # Einstellung in das globale Dict legen
#         _global_all_settings[name] = self
#
#
#     def __str__(self):
#         """
#         Gibt die UTF-8 Repräsentation des Einstellungsnamens zurück
#         """
#
#         return self.name.encode("utf-8")
#
#
#     def __unicode__(self):
#         """
#         Gibt die Unicode-Repräsentation des Einstellungsnamens zurück
#         """
#
#         return unicode(self.name)
#
#
#     def set(self, value):
#         """
#         Setzt die Einstellung.
#
#         Ist für die Einstellung ein Datenspeicher eingestellt
#         Speichert die Einstellung in
#         """
#
#
#     @property
#     def value(self):
#         """
#         """
#
#         return u"XXX"
#
#
#     # Ein Call der Einstellung gibt den Wert zurück
#     __call__ = value
#
#
#
#
#
#
