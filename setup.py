#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS - Setup
 
Created
    2013-02-16 by Gerold - http://halvar.at/
"""

import os
from setuptools import setup, find_packages, findall

THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)

VERSION = open("version.txt").readline().strip()
HOMEPAGE = "http://gerold-penz.github.com/python-simplecms/"
#DOWNLOAD_BASEURL = "https://cherrypy-cgiserver.googlecode.com/files/"
#DOWNLOAD_URL = DOWNLOAD_BASEURL + "cherrypy-cgiserver-%s.tar.gz" % VERSION


setup(
    name = "python-simplecms",
    version = VERSION,
    description = (
        "Simple Python CMS - Content Management System - Made Simple"
    ),
    long_description = open("README.rst").read(),
    keywords = "CherryPy Web Content Management System CMS",
    author = "Gerold Penz",
    author_email = "gerold@halvar.at",
    url = HOMEPAGE,
    # download_url = DOWNLOAD_URL,
    # packages = find_packages(),
#    data_files = [
#        ["./yyy", ["_git_add.py"]],
#    ],
    classifiers = [
        "Development Status :: 1 - Planning",
        #"Development Status :: 2 - Pre-Alpha",
        #"Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: CherryPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    ],
#    install_requires = [
#        "distribute",
#        "cherrypy"
#    ],
)

