from argparse import ArgumentParser
import json
import logging
from pathlib import Path
import pickle
import sys

log = logging.getLogger(__name__)

import validation
from viewer import Viewer

with Path('gopts.pkl').open('rb') as f:
    GLOBAL_OPTS = pickle.load(f)

print(f"{GLOBAL_OPTS=}")

DEBUG = GLOBAL_OPTS['debug']
VERBOSE = GLOBAL_OPTS['verbose']
PROGRAM = GLOBAL_OPTS['program']

if VERBOSE: print(f"running {PROGRAM}")

ARGS_FILE = Path(GLOBAL_OPTS['args_json_file'])
parser = ArgumentParser(PROGRAM, ARGS_FILE.read_text())
if ARGS_FILE.exists():
    with ARGS_FILE.open() as f:
        try:
            PARSER_ARGUMENTS = json.load(f)
        except json.JSONDecodeError:
            print_exc()
            PARSER_ARGUMENTS = None

if PARSER_ARGUMENTS:
    for arg in PARSER_ARGUMENTS:
        parser.add_argument(*arg[0], **arg[1])
    ARGS = parser.parse_args(sys.argv[1:])
else:
    ARGS = None

if ARGS: GLOBAL_OPTS = GLOBAL_OPTS.new_child(vars(ARGS))
DEBUG = GLOBAL_OPTS['debug']
VERBOSE = GLOBAL_OPTS['verbose']
PROGRAM = GLOBAL_OPTS['program']

if VERBOSE: print(f"SETTINGS: {GLOBAL_OPTS=}")

if DEBUG: log.debug(f' module loaded')


if __name__ == '__main__':
    log.debug(f' running {__name__}')
    print("Hello gcv")
    Viewer(GLOBAL_OPTS).run()
