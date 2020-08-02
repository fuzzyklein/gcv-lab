#! /usr/bin/env python3.8
# --*-- coding: utf-8 --*--
""" constants.py
    v0.0.0c

    This file defines commonly used character constants, etc.
"""
from collections import ChainMap
from configparser import ConfigParser
from enum import Enum
from inspect import currentframe, getmembers
import logging
import os
from os import listdir
from pathlib import Path
import re
import sys

from bs4 import BeautifulSoup
import requests

EMPTY = ""
PERIOD = '.'
NEWLINE = '\n'
UNDERSCORE = '_'
HYPHEN = '-'
COMMA = ','
SPACE = ' '
COLON = ':'
SEMICOLON = ';'
ELLIPSIS = '.' * 3
SLASH = '/'
TILDE = '~'
ASTERISK = '*'
LPAREN = '('
RPAREN = ')'
DOLLAR = '$'

UTF_8 = 'utf-8'
TREE = 'tree'

IGNORE_PATS = ['*.pyc', 'setup.py', "*__pycache__"]

####################################### DEPRECATION ZONE #######################

# USERDIR = Path.home()
# HOMEDIR = Path(__file__).resolve().parent.parent
# CONFDIR = HOMEDIR / "etc"
#
#
# SYS_CONFIG_DIR_NAME = ".etc"
# SYS_CONFIG_DIR_PATH = USERDIR / SYS_CONFIG_DIR_NAME
# SYS_CONFIG_FILE_NAME = "config.ini"
# SYS_CONFIG_FILE_STR = str(SYS_CONFIG_DIR_PATH / SYS_CONFIG_FILE_NAME)

# print(SYS_CONFIG_FILE_STR)

################################### END DEPRECATION ZONE #######################

BACKUP_SUFFIX = "~"

try:
    src = requests.get("https://docs.python.org/3/py-modindex.html").text
except:
    src = Path("/usr/share/doc/python3.7-doc/html").read_text()

class BS(BeautifulSoup):
    def __init__(self, s):
        super().__init__(s, features="html.parser")

PYTHON_MODULES = None
try:
    PYTHON_MODULES = {a.text.split('.')[0] for a in BS(src).findAll("a") if len(a.text) > 1 and not a.text[0].isupper()}
except:
    path = "usr/lib/python3.8"
    PYTHON_MODULES = list(sorted([n for n in listdir(path) if not n.startswith(PERIOD)], key=str.lower))

RUNNING_WINDOWS = os.name == 'nt'
SITE_PKG_DIR = sys.prefix + os.sep + ('Lib' if RUNNING_WINDOWS else 'lib/python3.8') + os.sep + 'site-packages'
PACKAGE_MODULES = sorted([re.sub(".py$", "", n) for n in listdir(SITE_PKG_DIR) if not re.search(".*-info", n)])

class FileType(Enum):
    UNKNOWN = 0
    PYTHON = 1
    BASH = 2

FILE_TYPES = { ".py": FileType.PYTHON, ".sh": FileType.BASH }
PYTHON_VERSION = '.'.join(sys.version.split()[0].split('.')[:2])

HILITE_ME = "http://hilite.me/api"

if __name__ == "__main__":
    print(f"Testing {__file__}...")
    try:
        import testing
    except ModuleNotFoundError:
        import py.testing
