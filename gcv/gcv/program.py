#! /usr/bin/env python3.8
# # Program
#
# Define a `Program` class.

from collections import ChainMap
from configparser import ConfigParser
import fileinput
import logging
import os
import os.path
from os import chdir as cd
from os import chdir, listdir
from pathlib import Path
import sys

# from py.arguments import Arguments
# from py.configuration import Configuration
# from py.constants import *
# from py.utilities import *

from startup import *

# Subclasses of `Program` should define `__init__` and/or `run` as needed.

class Program():
    """ Define a base class for classes that initialize a program and define its
        behavior.
    """
    def __init__(self, settings=None):
        """ Initialize the object. """
        self.settings = settings
        print("Initializing program...")
        if not self.settings:
            parser = ConfigParser()
            parser.read("etc/config.ini")
            self.settings = parser["DEFAULT"]
            self.settings = ChainMap(self.settings, parser["DEFAULT"])
            parser.read("www/etc/jupyter.ini")
            self.settings = ChainMap(self.settings, parser["DEFAULT"])
            PY_DIR = self.settings["py_directory"]
        if self.settings["verbose"]: print(f'{self.settings=}')

        # self.log.info("Getting input text...")
        # self.get_input()
        # self.process_args()
        if self.settings["verbose"]: print("program initialized.")

    def run(self):
        """ Override this method to provide all the application code if using this class for a command line script. """
        if self.settings["verbose"]: self.output("Calling `Program.run()`")

    def output(self, s):
        """ This method can be overridden, especially for PyGTK+ programs. """
        print(s)

    def get_input(self):
        """ Check for standard input coming in through a pipe. """
        args = sys.argv[1:]
        for f in sys.argv[1:]:
            p = Path(f)
            if (not p.exists()) or p.is_dir() or (not p.is_file()):
                args.remove(f)
            if p.is_dir() and self.settings["recursive"]:
                for d in os.walk(p):
                    for f2 in d[2]:
                        if not ignore(f2):
                            args.append(os.path.join(d[0], f2))
        self.settings["input text"] = dict()
        with fileinput.input(args) as cin:
            current_file = None
            for line in cin:
                try:
                    new_file = cin.filename()
                    if new_file != current_file:
                        current_file = new_file
                        self.settings["input text"][current_file] = list()
                    self.settings["input text"][current_file].append(line.rstrip('\n'))
                except FileNotFoundError:
                    if self.settings["verbose"]:
                        print(f"file {f.filename()} not found!")

    def process_args(self):
        if "args" in self.settings.keys():
            for f in self.settings["args"]:
                assert(type(f) is str)
                self.process_fname(f)

    def process_fname(self, s):
        p = Path(s)
        if not p.exists():
            if self.settings["verbose"]:
                print(f"File {s} does not exist.")
                return
        elif p.is_symlink():
            self.process_link(p)
        elif p.is_dir():
            self.process_dir(p)
        elif p.is_file():
            self.process_file(p)

    def process_link(self, p):
        if not self.settings["follow"]:
            if self.settings["verbose"]:
                print(f"File {s} is a symbolic link.")
                return
            else:
                pass
        else:
            process_file(p)

    def process_dir(self, p):
        if not ignore(p):
            if self.settings["verbose"]:
                print(f"Processing directory {str(p)}")
            if self.settings["recursive"]:
                for f in listdir(str(p)):
                    self.process_fname(os.path.join(str(p), f))

    def process_file(self, p):
        global log
        log.debug(f"Program is processing file {p}")
        if not ignore(p):
            if self.settings["verbose"]:
                print(f"Processing file {str(p)}.")

__all__ = ["Program"]

if __name__ == "__main__":
    print(f"Testing {__file__}...")
    try:
        import testing
    except ModuleNotFoundError:
        import py.testing


# ## References

# * [ConfigParser](https://docs.python.org/3.7/library/configparser.html#configparser.ConfigParser)
# * [ArgumentParser](https://docs.python.org/3.7/library/argparse.html#argparse.ArgumentParser)
