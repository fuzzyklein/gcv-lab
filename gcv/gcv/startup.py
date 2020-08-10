# -*- coding: utf-8 -*-
""" # Idle/Jupyter Startup File

    Defines functions for use in `IDLE`, but so far they seem to work in `python3`,
    `iPython`, `IDLE`, and `jupyter`.

    They WON'T work in Python 2! Hopefully this won't cause problems when
    PYTHONSTARTUP is set to this file's path, but it may very well happen.
    
    Many of the objects imported by this module are useful inside an interpreter
    environment like Jupyter, so it's recommended to import this file by executing
    it:
    
        `exec(Path("startup.py").read_text())`

"""
from __future__ import annotations
from cmd import Cmd
from collections import ChainMap, namedtuple
from configparser import ConfigParser
import cProfile
import csv
from enum import Enum
import fnmatch
from functools import singledispatch, singledispatchmethod
import glob
from importlib import import_module, reload
import inspect
from inspect import currentframe, getmembers
from math import floor, log10
import os
from os import chdir, curdir, getenv, listdir, mkdir
from pprint import pprint
pp = pprint
from pathlib import Path
import re
import shlex
from shutil import copy2 as copy, copytree, ignore_patterns, move, rmtree
import string
from subprocess import check_output
import sys
from xml.dom.minidom import Document
import webbrowser

from bash import bash
from bs4 import BeautifulSoup
#import file as magic
from IPython.display import display, HTML
import pandas as pd
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

IGNORE_FILES = ['*.pyc', 'setup.py']
IGNORE_DIRS = ["*__pycache__", ".git", "build", "dist", "*.egg-info", ".ipynb_*", ".*", "_*"]
IGNORE_PATS = list(set(IGNORE_FILES).union(IGNORE_DIRS))

try:
    src = requests.get("https://docs.python.org/3/py-modindex.html").text
except:
    src = Path("/usr/share/doc/python3.7-doc/html/py-modindex.html").read_text()

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
BACKUP_SUFFIX = '+' if RUNNING_WINDOWS else "~"


class FileType(Enum):
    UNKNOWN = 0
    PYTHON = 1
    BASH = 2

FILE_TYPES = { ".py": FileType.PYTHON, ".sh": FileType.BASH }
PYTHON_VERSION = '.'.join(sys.version.split()[0].split('.')[:2])

HILITE_ME = "http://hilite.me/api"

PYTHON_MOD_INDEX = 0
PACKAGE_MOD_INDEX = 1
LOCAL_MOD_INDEX = 2

FILES = [
    "__init__.py",
    "testing.py",
    "constants.py",
    "percentage.py",
    "startup.py"
]

class BS(BeautifulSoup):
    def __init__(self, s):
        super().__init__(s, features="html.parser")

def get_interpreter():
    """ Return the currently active interpreter as a string Enum.
    """
    f = currentframe().f_back.f_code.co_filename
    # print("File:", f)
    if re.match('<pyshell#\d*>', f):
        return("idle")
    elif re.match("<ipython-", f):
        f2 = currentframe().f_back.f_back
        if f2 and f2.f_code.co_filename.endswith('IPython/core/interactiveshell.py'):
            if sys.stdin.isatty():
                return "ipython"
            else:
                return "jupyter"
    return "script" if f else "stdin"

@singledispatch
def num_digits(x: object):
    print(f"bad argument: num_digits: {x}")
    
@num_digits.register
def _(i:int) -> int:
    """ Assumes that i is an integer and not a float.
    """
    return int(floor(log10(i)) + 1)

def get_all(path, ignore=set()):
    """ Get the names of all the variables, classes and functions defined within
        a module.
    """
    result = set()
    if type(path) is str:
        path = Path(path)
    lines = path.read_text().split('\n')
    regex = re.compile("def (\w*)|class (\w*)|(\w*)\s+=")
    for s in lines:
        m = regex.match(s)
        if m:
            i = 1
            while not m.group(i):
                i += 1
            assert i < 4
            word = m.group(i)
            if word and not word.startswith('_'):
                result.add(word)
    return sorted(list(result.difference(ignore)))

def ignore(filename):
    """ Return `True` if `filename` is included in the `list` `constants.IGNORE_PATS`
        and `False` otherwise.

        >>> ignore('*.pyc')
        True

        >>> ignore('*.js')
        False
    """
    for pat in IGNORE_PATS:
        if fnmatch.fnmatch(filename, pat):
            return True
    return False

def run(s: str)->str:
    """ Run `s` as a command line. `s` is a `str`, not a `list`. """
    return check_output(shlex.split(s), encoding=UTF_8) or None


def runfile():
    """ TODO: write `startup.runfile` """
    pass

def columnize(s):
    """ Print the contents of the list `s` in neat-looking columns. """
    if s:
        Cmd().columnize(list(s))
    else:
        print("None")
        
def ls(*paths, all=False, recursive=False, out=True):
    paths = list(paths)
    if not paths:
        paths.append(PERIOD)
    for path in paths:
        if recursive:
            value = run(TREE + (" -a" if all else EMPTY) + SPACE + (str(path) if path else EMPTY))
            print(value)
        else:
            columnize(sorted([n for n in listdir(path if path else Path.cwd())
                                if ((not n.startswith(PERIOD)) if not all else True)
                             ], key=str.lower))

cd = chdir

def tree(path=None, all=False):
    ls(path, all=all, recursive=True)

def pwd():
    print(Path.cwd())

def touch(s: str):
    Path(s).touch()

def public(obj):
    columnize([member for member in dir(obj) if not re.match('_', member)])

def cat(*paths):
    for path in paths:
        if type(path) is str: path = Path(path)
        if path.exists() and path.is_file():
            print(path.read_text())

def find(pattern="*", topdir=Path.cwd(), recursive=True):
    """ Print the path to any files whose names match `pattern` in any
        subdirectory of `topdir` if `recursive` is `True` and only `topdir` if
        it's `False`.
    """
    paths = set()
    if type(topdir) is str: topdir=Path(topdir)
    if not recursive:
        paths = {name for name in listdir() if fnmatch.fnmatch(name, pattern)}
        # pp([name for name in listdir() if fnmatch.fnmatch(name, pattern)])
    else:
        for path in topdir.iterdir():
            if path.is_dir(): paths = paths.union(find(pattern, path, recursive))
            elif path.is_file() and fnmatch.fnmatch(path.name, pattern):
                # print(path)
                paths.add(path)
    return paths

@singledispatch
def grep(PATTERN,  # `str`, a compiled pattern or a list of either
         *GLOBS,   # `str` representing a `glob` pattern or a list of them
         **options):
    """ Search for `PATTERN: re.Pattern` in each file whose name matches a pattern in `FILES`.
        
    """
    try:
        return grep(re.compile(str(PATTERN)), *GLOBS, **options)
    except:
        print(f"ERROR: grep: bad argument type: {type(PATTERN)}")
    

grep.DEFAULTS = {
    "fixed": False,     # fixed list of strings
    "basic": True,      # PATTERN is a basic regular expression
    "perl": False,      # PATTERN is a Perl regexp
    "pattern": None,    # use this as the pattern
    "file": None,       # get a list of patterns from the file
    "case": True,       # default search displays case-sensitivity
    "invert": False,    # return non-matching lines
    "word": False,      # select only lines that match whole words
    "line": False,      # select only lines that match entirely
    "count": False,     # print only a count of matching lines for each file
    "color": False,     # print colored output if possible
    "match": False,     # output filenames with matches
    "matchless": False, # output filenames without matches
    "max": None,        # stop reading a file after N matches
    "only": False,      # print only the matched (non-empty) parts of a matching line, each such part on a separate output line
    "quiet": False,     # don't output anything
    "errors": True,     # output error messages for non-existent or unreadable files
    "bytes": False,     # output the byte offset with respect to the file before each line
    "fname": True,      # print the file name for each match
                        # default to True if searching more than one file
                        # default to False if there is only one file or only stdin to search
    "label": None,      # display input from stdin as coming from the given file
    "number": True,     # display the line number of each match
    "tab": None,        # if True, prefix actual line output with a tab
                        # if a `str`, use it instead of a tab
    "text": False,      # process a binary file as if it were text
    "binary": None,     # assume that binary files are of the given type
    "device": input,    # action to process a device
    "directory": grep,  # action to process a directory
    "exclude": list(),  # list of filename patterns to be excluded or a Path to a file that lists them
    "include": list(),  # list of filename patterns to be included in the search
    "recursive": False, # read all files under each directory recursively
    "follow": False,    # follow all symbolic links

}

@grep.register
def _(PATTERN: str, *args, **kwargs):
    return grep(re.compile(PATTERN), *args, **kwargs)


@grep.register
def _(PATTERN: list, *args, **kwargs):
    value = list()
    for p in PATTERN:
        value.extend(grep(p, *args, **kwargs))
    return value

@grep.register
def _(PATTERN: re.Pattern, # `str`, a compiled pattern or a list of either
      *GLOBS,              # `str` representing a `glob` pattern or a list of them
      **options            # keyword arguments
    ):
    """ Search for `PATTERN: re.Pattern` in each file whose name matches a pattern in `FILES`.
        
    """
    options = ChainMap(options, grep.DEFAULTS)
    
    results = dict()
    for g in GLOBS:
#         print(f"{g=}")
        for f in iglob(g, recursive=options["recursive"]):
            f = Path(f)
#             print(f"{f=}")

            try:
                value = list()
                if f.is_dir() and options["recursive"]:
                    value.extend(grep(PATTERN, f.name, **options))
                elif f.is_file() and not any([fm.fnmatch(f.name, p) for p in options["exclude"]]):
                    for i, line in enumerate(f.read_text().split('\n')):
                        if PATTERN.search(line):
                            value.append(GrepMatch(i, line))
                results[f] = value
            except UnicodeDecodeError:
                print(f"unicode error: file {f}")

    if not options["quiet"]:
        for k, v in results.items():
            print(f"File: {k}\n")
            for i, line in enumerate(v):
                print(f"{v[i].lineno}: {v[i].line}")
            print()

        
    else: return results

def cut(inList, delim=SPACE, indices=[]):
    if issubclass(type(inList), str):
        inList = Path(inList)
    if issubclass(type(inList), Path):
        inList = inList.read_text().split('\n')
    if not indices: indices = [i for i in range(len(inList))]
    result = None
    if inList:
        result = list()
        for l in inList:
            subString = str()
            for w in l.split(delim):
                for i in indices:
                    if type(i) is int:
                        subString += w
                    else:
                        for i in range(indices[i][0], indices[i][1]):
                            subString += SPACE + w
                result.append(subString)
    return result

SearchAndReplace = namedtuple("SearchAndReplace", ["pattern", "replace"])

class Replacement(SearchAndReplace):
    pass

class ReplacementList(list):
    pass

def sed(lines, *args, all=True, inplace=False):
    """ Substitute occurences of `pattern` with `replace` in the file `path`. """
    if issubclass(type(lines), Path):
        text = lines.read_text().split('\n')
    else:
        text = copy(lines)
    if type(args[0]) is str:
        arguments = ReplacementList()
        for i in range(0, len(args), 2):
            repl = Replacement(args[i], args[i+1])
            arguments.append(repl)
        args = arguments
    for i, sr in enumerate(args):
        print(f"Pattern: {sr.pattern}")
        print(f"Replacement: {sr.replace}")
        for j, line in enumerate(text):
            line2 = re.sub(sr.pattern, sr.replace, line)
            print(f"{line} ==>\n{line2}")
            text[j] = line2
            if line2 != line and not all:
                break
    text = '\n'.join(text)
    print(text)
    if issubclass(type(lines), Path) and inplace:
        Path(lines.parent / (lines.name + inplace)).write_text(lines.read_text())
        print("Writing sed output to file")
        lines.write_text(text)


def sort():
    pass

def uniq():
    pass

def profile(s):
    cProfile.run(s)

def backup(d:Path=Path.cwd())->Path:
    """ Copy the entire current directory to `../<DIR>~/`. """
    BACKUP_DIR_NAME = str(d) + BACKUP_SUFFIX
    if Path(BACKUP_DIR_NAME).exists(): rmtree(BACKUP_DIR_NAME)
    copytree(str(d), BACKUP_DIR_NAME, ignore=ignore_patterns(*IGNORE_PATS))
    print(f"{BACKUP_DIR_NAME=}")
    print(f"{d=}")       
    return Path(BACKUP_DIR_NAME)

def clean(s=None):
    """ Clean the current working directory by default or the one targeted by
        `s`.
    """

def config(path):
    """ Return a dictionary containing the keys and values of the given file. """
    if type(path) is str:
        path = Path(path)
    if path.exists():
        cp = ConfigParser()
        cp.read(str(path))
        return dict(cp["DEFAULT"])
    else:
        return None

def docs(obj=None):
    """ Some automatic detective work could be done here to determine where to
        find the latest documentation.

        # TODO:

        * Determine which version of Python is actually running.
        * Search `/usr/share/doc` for `python-{version}-doc/html/index.html`.
        * If that file exists, open it in a Web browser.
        * If that file doesn't exist, try to open its remote counterpart online.
        * If that fails, work backwards through 3.7, 3.6, 3.5, etc. until a
        * suitable version can be found.
        * If all that fails, then the computer is not hooked up to the Internet
          and has no online documentation installed locally. Pydoc might have
          an answer for that.

    """
    if not obj:
        webbrowser.open("file:///usr/share/doc/python3.7/html/index.html")
    else: #TODO: Fix this because the line below only works for modules or something like that.
        run("pydoc3 -w {} ".format(str(type(obj))))

def open_src_file(s):
    if issubclass(type(s), Path):
        s = str(s)
    run("atom" + SPACE + s)

def slurp(s):
    if issubclass(type(s), str):
        s = Path(s)
    return s.read_text()
    return None

def get_imports(path=Path.cwd(), recursive=True):
    """ Return a `set` containing the names of the modules imported by `path`.
    """
    FILES = glob.iglob(str(path / "*.py"), recursive=recursive)
    LOCAL_MODULES = sorted([n.stem for n in FILES if not n.stem.startswith(PERIOD)], key=str.lower)
    # print(f'{LOCAL_MODULES=}')
    results = [set(), set(), set()]
    if type(path) is str:
        path = Path(path)
    if path.is_dir():
        for f in find("*.py", path):
            result = get_imports(f)
            results = [r.union(result[i]) for i, r in enumerate(results)]
    else:
        result = set()
        lines = path.read_text().split('\n')
        regex = re.compile("\s*import (\w*)|\s*from (\w*)")
        for s in lines:
            m = regex.match(s)
            if m:
                i = 1
                while not m.group(i):
                    i += 1
                assert i < 4
                word = m.group(i)
                if word:
                    m2 = re.search(r'(\w*)\.\w*', word)
                    if m2:
                        word = m2.group(1)
                    result.add(word)
        for r in result:
            if r in PYTHON_MODULES:
                results[0].add(r)
            elif r in LOCAL_MODULES:
                results[2].add(r)
            else:
                # if not r == "py"
                results[1].add(r)
        results = [sorted(list(r)) for r in results]
    return results

def print_imports(path=Path.cwd()):
    results = get_imports(path)
    if len(results[0]):
        print("Python Modules:")
        print()
        columnize(results[0])
        print()
    if len(results[1]):
        print("Packages:")
        print()
        columnize(results[1])
        print()
    if len(results[2]):
        print("Local Modules:")
        print()
        columnize(results[2])
        print()

def csv2html(path=None, code=False):
    """ Read a (specially designed) CSV file and return it as HTML.

        TODO: Handle the first row specially and optionally.
    """
    if type(path) is str:
        path = Path(path)
    with path.open() as f:
        reader = csv.reader(f)
        output = '<table>'
        for i, row in enumerate(reader):
            if code:
                row[0] = "<code>" + row[0] + "</code>"
            output+=('<tr><td>{}</td></tr>\n'
                  .format("</td><td>".join(row)))
        output+=("</table>\n")

        # print( output)
        return output

def hilite_src_lines(obj):
    codeStr = inspect.getsource(obj)
    hilite_params = { "code": codeStr }
    return requests.post(HILITE_ME, hilite_params).text

def get_desc(s):
    """ Return the first line of the docstring of the object named by `s`.
    """
    print(s)
    print()
    print(f"{vars().keys()=}")
    return inspect.getdoc(vars()[s]).split('\n')[0]

def describe(p: Path) -> str:
    """ Return a HTML table of function names and their descriptions.

        Get the description of each function from the first line of its docstring.
    """
    rowData = list()
    desc = ''
    for s in get_all(Path("startup.py")):
        if not s[0].isupper():
            desc = inspect.getdoc(globals()[s])
            if desc:
                desc = desc.split('\n')[0] if desc else ''
            rowData.append((s, desc))
    doc = Document()
    table = doc.createElement("table")
#     doc.appendChild(table)
    for d in rowData:
        row = doc.createElement("tr")
        cell = doc.createElement("td")
        tag = doc.createElement("code")
        link = doc.createElement("a")
        text = doc.createTextNode(d[0])
        p2 = Path("d[0]")
        tag.appendChild(text)
        cell.appendChild(tag)
        row.appendChild(cell)
        cell = doc.createElement("td")
        tag = doc.createElement("p")
        text = doc.createTextNode(d[1] if d[1] else '')
        tag.appendChild(text)
        cell.appendChild(tag)
        row.appendChild(cell)
        table.appendChild(row)
    return table.toxml()

def hilite_definition(obj):
    if not type(obj) is str: obj = obj.__name__
    src = grep(obj + " = ", files='*.py', quiet=True)
    for k, v in src.items():
        if k.name in FILES:
            line = v[1]
            hilite_params = {'code': line}
            LOCATION = f"<p><code>{obj}</code> is defined in <code>{k.name}</code>.</p>\n"
            return LOCATION + requests.post(HILITE_ME, hilite_params).text
    return None

def get_class_names(p:Path)->list:
    return [s for s in get_all(p) if s[0].isupper() and not s[1].isupper()]

def highlight(obj):
    display(HTML(hilite_definition(obj) if type(obj) is str else hilite_src_lines(obj)))
    
if __name__ == '__main__':
    print("hello world")
