#!/usr/bin/env python
# coding: utf-8
"""
Sprache und Lokalisierung
"""

import cherrypy
import config
import cookie


def get_fallback_language():
    """
    Gibt das Kürzel der Standardsprache des CMS zurück.
    Das ist die erste Sprache in der Sprachen-Liste.
    """

    return config.LANGUAGES.value[0]


def get_accepted_language_codes(firstshot = False):
    """
    Findet heraus, welche Sprache eingestellt wurde und gibt eine Liste mit
    möglichen Ländercodes, sortiert nach Priorität, zurück.

    Zuerst wird in der URL nachgesehen, ob eine Sprache angefordert wird.
    Wenn nicht, dann wird das Language-Cookie ausgewertet.
    Dann wird der Request nach der Spracheinstellung des Browsers durchsucht.

    Wird die Sprache über die URL übergeben, dann wird diese zusätzlich in das
    Language-Cookie geschrieben.

    :param firstshot: Wenn True, dann wird die erste mögliche Sprache zurück
        geliefert. Es wird nicht lange nach anderen Sprachen gesucht.
    """

    LANGUAGE_CODES = config.LANGUAGES.value

    language_code = None
    lang_items = []

    # Path Info
    path_list = [ item for item in cherrypy.request.path_info.split("/") if item ]
    if path_list:
        if path_list[0] in LANGUAGE_CODES:
            language_code = path_list[0]
            if firstshot:
                return [language_code]
            lang_items.append([3.0, language_code])
            # Neue Sprache in das Language-Cookie eintragen
            cookie.set_cookie(cookie.LANGUAGE, language_code)

    # Language-Cookie
    if not language_code:
        lang_cookie = cookie.get_cookie(cookie.LANGUAGE)
        if lang_cookie in LANGUAGE_CODES:
            language_code = lang_cookie
            if firstshot:
                return [language_code]
            lang_items.append([2.0, language_code])

    # Browser
    accept_language = cherrypy.request.headers.get("ACCEPT-LANGUAGE")
    accept_language.replace("-", "_").lower()
    if accept_language:
        # Möglichkeit 1: da, en-gb;q=0.8, en;q=0.7
        # Möglichkeit 2: de-de;q=1.0,de;q=0.8,en-us;q=0.5,en;q=0.3
        raw_items = [
            item.strip() for item in accept_language.split(",") if item.strip()
        ]
        for raw_item in raw_items:
            if ";" in raw_item:
                try:
                    lang, q = [
                        item.strip() for item in raw_item.split(";", 1) if item.strip()
                    ]
                    lang_items.append([float(q.split("=")[1].strip()), lang])
                except IndexError:
                    pass
            else:
                lang_items.append([1.0, raw_item])

    # Standardsprache anhängen
    lang_items.append([0.0, LANGUAGE_CODES[0]])

    # Einträge nach Priorität sortieren und zurück geben
    lang_items.sort(reverse = True)
    ret_items = []
    for lang_item in lang_items:
        if lang_item[1] in LANGUAGE_CODES:
            if lang_item[1] not in ret_items:
                ret_items.append(lang_item[1])
    return ret_items


# def get_current_language():
#     """
#     Gibt die aktuelle Spracheinstellung für den Request zurück
#     """
#
#     return get_accepted_language_codes(firstshot = True)[0]
#
#
# def get_translation_obj(language = None):
#     """
#     Gibt das für die aktuelle Sprache zuständige *gettext.translation*-Objekt
#     zurück
#
#     :param language: Wenn None, dann wird die Sprache mit `get_current_language()`
#         ermittelt. Wenn angegeben, dann wird die hier angegebene Sprache für die
#         Übersetzung verwendet.
#     """
#
#     if language:
#         current_language = language
#     else:
#         current_language = get_current_language()
#
#     if len(current_language) <= 2:
#         languages = [current_language]
#     else:
#         languages = [current_language, current_language[:2]]
#
#     return gettext.translation(
#         LOCALEDOMAIN_TEMPLATES, localedir = LOCALEDIR,
#         languages = languages, fallback = True
#     )
