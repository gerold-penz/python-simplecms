#!/usr/bin/env python
# coding: utf-8
"""
Simple Python CMS - Setup
 
Created
    2013-02-16 by Gerold - http://halvar.at/
"""

import os
import sys
import distutils.core
from setuptools import setup, find_packages

# Upload zu Google-Code
# http://code.google.com/p/support/source/browse/#svn%2Ftrunk%2Fscripts
try:
    from googlecode_upload.googlecode_distutils_upload import upload
except ImportError:
    class upload(distutils.core.Command):
        user_options = []
        def __init__(self, *args, **kwargs):
            sys.stderr.write(
                "error: Install this module in site-packages to upload: \n"
                "http://support.googlecode.com/svn/trunk/scripts/googlecode_distutils_upload.py"
            )
            sys.exit(3)

THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)

VERSION = open("version.txt").readline().strip()
HOMEPAGE = "http://gerold-penz.github.com/python-simplecms/"
DOWNLOAD_BASEURL = "https://python-simplecms.googlecode.com/files/"
DOWNLOAD_URL = DOWNLOAD_BASEURL + "python-simplecms-%s.tar.gz" % VERSION


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
    download_url = DOWNLOAD_URL,
    packages = find_packages(),
    classifiers = [
        "Development Status :: 1 - Planning",
        #"Development Status :: 2 - Pre-Alpha",
        #"Development Status :: 3 - Alpha",
        #"Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: CherryPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    ],
    install_requires = [
#        "distribute",
        "cherrypy",
        "redis"
    ],
    cmdclass = {"upload": upload},
)

