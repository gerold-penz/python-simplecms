#!/usr/bin/env python
# coding: utf-8
"""
Globale Konstanten
"""

import os

# Basisordner
THISDIR = os.path.dirname(os.path.abspath(__file__))
APPDIR = THISDIR
HTTPROOTDIR = os.path.join(APPDIR, "http_root")

# Content-Typen mit Textinhalt
CONTENT_TYPES_TEXT = {
    "text/plain",
    "text/html"
}

# Content-Typen die beim Speichern nicht komprimiert werden sollten
CONTENT_TYPES_NOT_COMPRESSIBLE = {
    "application/gzip",
    "application/zip",
    "application/zlib",
    "application/epub+zip",
    "application/lha",
    "application/lzx",
    "application/ogg",
    "application/vnd.ms-cab-compressed",
    "application/vnd.rn-realmedia",
    "application/x-ace-compressed",
    "application/x-bzip",
    "application/x-bzip2",
    "application/x-cab-compressed",
    "application/x-cbr",
    "application/x-deb",
    "application/x-compressed",
    "application/x-gzip",
    "application/x-lha",
    "application/x-lzh",
    "application/x-lzma",
    "application/x-lzx",
    "application/x-rar-compressed",
    "application/x-zip-compressed",

    "audio/aac",
    "audio/aacp",
    "audio/flac",
    "audio/mp4",
    "audio/mpeg",
    "audio/mpeg4-generic",
    "audio/ogg",
    "audio/vorbis",
    "audio/x-matroska",
    "audio/x-musepack",
    "audio/x-pn-realaudio",

    "image/gif",
    "image/jpeg",
    "image/pjpeg",
    "image/jp2",
    "image/png",
    "image/jpm",
    "image/jpx"
    "image/x-jg",
    "image/x-quicktime",

    "multipart/x-gzip",

    "video/H261",
    "video/H263",
    "video/H263-1998",
    "video/H263-2000",
    "video/H264",
    "video/H264-RCDO",
    "video/H264-SVC",
    "video/JPEG",
    "video/jpeg2000",
    "video/mp4",
    "video/MP4V-ES",
    "video/mpeg",
    "video/mpeg4-generic",
    "video/ogg",
    "video/quicktime",
    "video/x-motion-jpeg",
}
