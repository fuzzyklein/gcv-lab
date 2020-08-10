"""@package gcv

Parse a `gcode` file and display its path using `matplotlib`.
Generate `gcode` from various sources of input, including graphics and mathematical
expressions.
"""
from collections import ChainMap
from configparser import ConfigParser
import logging
import os
from pathlib import Path
import pickle
from pprint import pprint as pp
import re
import sys

try:
    from constants import *
except ModuleNotFoundError:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from constants import *

GLOBAL_OPTS = {'debug' : False, 'verbose' : False}
DEBUG = GLOBAL_OPTS['debug']
if DEBUG:
    GLOBAL_OPTS['verbose'] = True
VERBOSE = GLOBAL_OPTS['verbose']

LOGFILE = BASEDIR / 'log/errors.log'
print(f"{LOGFILE=}")
assert(BASEDIR.exists())
print(f"{BASEDIR=}")
if not LOGFILE.exists():
    print("Log does not exist:",f"{LOGFILE}")
    LOGDIR = LOGFILE.parent
    print(F"{LOGDIR=}")
    if not LOGDIR.exists():
        print("creating log directory:{LOGDIR}")
        LOGDIR.mkdir()
    print("creating log file")
    LOGFILE.touch()
    print('log file created')
if DEBUG:
    log_level = logging.DEBUG
elif VERBOSE:
    log_level = logging.INFO
else: log_level = logging.WARNING
logging.basicConfig(filename=str(LOGFILE), level=log_level, filemode='w')
log = logging.getLogger("root")
logging.captureWarnings(True)
if DEBUG: logging.debug(f" loading {__name__} module")

VERBOSE = GLOBAL_OPTS['verbose']
if VERBOSE: print(f"current working directory: {Path.cwd()}")
if VERBOSE: print(f"base directory: {BASEDIR}")
sys.path.insert(0, str(BASEDIR))
GLOBAL_OPTS['basedir'] = BASEDIR
if VERBOSE: print(f"{GLOBAL_OPTS=}")
if VERBOSE: print('system path');pp(sys.path)

CONFIG_DIR = BASEDIR / 'etc'
if CONFIG_DIR.exists():
    CONFIG = ConfigParser()
    CONFIG.read(CONFIG_DIR.rglob('*.ini'))
    if VERBOSE: print(CONFIG)
    for s in CONFIG.keys():
        for t in CONFIG[s].keys():
            GLOBAL_OPTS[t] = CONFIG[s][t]
elif DEBUG:
    logging.warning("configuration directory is missing")
if RUNNING_WINDOWS: GLOBAL_OPTS['packages_dir'] = str(BASEDIR.parent.parent.resolve())
if VERBOSE: print("SETTINGS:");pp(GLOBAL_OPTS)
SETTINGS = ChainMap({k:v for k,v in os.environ.items()
                         if re.match(r'GCV|gcv',k)},
                     GLOBAL_OPTS)

GLOBAL_OPTS_FILE = BASEDIR / 'gopts.pkl'
with GLOBAL_OPTS_FILE.open('wb') as f:
    pickle.dump(SETTINGS, f)
