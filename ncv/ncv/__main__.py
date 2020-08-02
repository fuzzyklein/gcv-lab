""" __main__.py

    Execute the package as a module:

        `$: python3.8 -m hw3 -v -t`
"""
from argparse import ArgumentParser
from cmd import Cmd
from collections import ChainMap
from configparser import ConfigParser
import json
import logging
from os import environ
from pathlib import Path
import re
import sys
from traceback import print_exc
import warnings

# Set the filters for the warnings system. This may be a different setting for
# development and release versions.
warnings.simplefilter('default')

CONFIG_FILE = 'etc/config.ini'
ARGS_FILE = 'json/arguments.json'
CONFIG = ConfigParser()
CONFIG.read(CONFIG_FILE)

PROGRAM = CONFIG["DEFAULT"]["program"]

ENVIRONMENT = {k : v for k, v in environ.items() if k[0].islower()}

parser = ArgumentParser(PROGRAM, Path(CONFIG["ARGUMENTS"]["epilog"]).read_text())
f = open(ARGS_FILE)
try:
    PARSER_ARGUMENTS = json.load(f)
except json.JSONDecodeError:
    print_exc()
    PARSER_ARGUMENTS = None
    exit(1)
f.close()

if PARSER_ARGUMENTS != None:
    for arg in PARSER_ARGUMENTS:
        parser.add_argument(*arg[0],**arg[1])
    ARGS = parser.parse_args(sys.argv[1:])
else:
    ARGS = None

CATEGORIES = list()
for s in Path(CONFIG_FILE).read_text().split('\n'):
    m = re.match(r'\[(\w*)\]', s)
    if m:
        CATEGORIES.append(m.group(1))
SETTINGS = ChainMap(ENVIRONMENT, *[CONFIG[s] for s in CATEGORIES])
if ARGS: SETTINGS = SETTINGS.new_child(vars(ARGS))
# SETTINGS = dict(ChainMap(vars(ARGS), ENVIRONMENT, *[CONFIG[s] for s in CATEGORIES])) \

LOGFILE = SETTINGS["logfile"]
log_level = logging.WARNING
if SETTINGS["verbose"]:
    log_level=logging.INFO
if SETTINGS["debug"]:
    log_level=logging.DEBUG
logging.basicConfig(filename=LOGFILE, level=log_level, filemode='w')
log = logging.getLogger("root")
logging.captureWarnings(True)
logging.debug(f"loading {__name__} module")

if SETTINGS["verbose"]: print("Loading `hw3` in verbose output mode...")

logging.debug(f"{__name__} module loaded")

from ncv.ncviewer import NCViewer

def main():
    """ main()

        Call the `run` method of a class descended from `py.Program`.

    """
    logging.debug(" running `main`")
    global SETTINGS

    if SETTINGS["verbose"]: print("Running", PROGRAM, '...')

    # from hw3.program import Program
    NCViewer(SETTINGS).run()

if __name__ == "__main__":
    if SETTINGS["testing"]:
        print(f"Testing {__file__}...")
        import doctest
        doctest.testmod(optionflags=doctest.ELLIPSIS)
    else:
        main()
