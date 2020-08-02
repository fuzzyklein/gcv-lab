#! /usr/bin/env python3.6
import fnmatch
from pdb import set_trace
import sys
import unittest

try:
    from py.utilities import find, run
except ModuleNotFoundError:
    sys.path.insert(0, "py")
    from utilities import find, run


class Tester(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass

    def test_all(self):
        for f in find("*.py"):
            if not f.stem in {"setup", "testing", "backup", "cleandir",
                              "colors", "tools", "more", "build", "py2jnb",
                              "__idlestartup__", "template", "connection"}:
                print(run(f"python3.8 {str(f)}"))
