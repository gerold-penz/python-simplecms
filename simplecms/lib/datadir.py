#!/usr/bin/env python
# coding: utf-8
"""
Zugriff auf den Datenordner (datadir)

Created 2013-02-21 by Gerold - http://halvar.at/
"""

import os
import shutil



_global_data_directory = None


def init(data_directory):
    """

    """

    global _global_data_directory


    # # Datenbankordner erstellen, falls dieser noch nicht existiert
    # if not os.path.isdir(DATABASEDIR):
    #     os.makedirs(DATABASEDIR)
