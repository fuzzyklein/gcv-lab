""" # driver

    Define a generic Driver class with some basic functionality built in.
"""
from cmd import Cmd
import fileinput
import logging
import os
import os.path
from os import chdir, listdir
from pathlib import Path
import re
import shlex
from subprocess import check_output
import sys
from traceback import print_exc

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.addHandler(logging.NullHandler())
log.debug(f"loading {__name__} module")

from ncv.constants import *
from ncv.startup import *

class Driver(Cmd):
    """ Define a base class for classes that initialize a program and define its
        behavior.
    """
    def __init__(self, settings=None):
        """ Initialize the object. """
        super().__init__()
        s = repr(type(self))[:-2].split(PERIOD)[-1]
        self.prompt = LPAREN + s + RPAREN + COLON + SPACE
        if settings:
            self.settings = settings
        else:
            self.settings = dict() # this should never happen, but ...
            self.settings.update({"verbose": False})

        logging.debug(settings)

    def do_quit(self, args):
        """Exit the program. """
        yes = {"Yes", "yes", "Y", "y"}
        response = input("Are you sure you want to quit? ")
        if response in yes: return True
        return False

    def do_exit(self, args):
        return self.do_quit(args)

    def do_bye(self, args):
        return self.do_quit(args)

    def do_EOF(self, args):
        print()
        return True

    def preloop(self):
        if self.settings["verbose"]: print ("Initializing driver...")
        return False

    def postloop(self):
        if self.settings["verbose"]: print ("Closing driver ...")
        return True

    def do_settings(self,args):
        print("Settings:")
        pprint(self.SETTINGS)

    def do_sysinfo(self, args):
        print("Architecture: ".format(check_output(["arch"])))
        print("Version Info: {}".format(sys.version_info))
        print("Version: {}".format(sys.version))
        print("Platform: {}".format(sys.platform))

    def do_now(self, args):
        print(now())

    def do_cal(self, args):
        NOW = dt.now()
        print(calendar.TextCalendar().formatmonth(NOW.year, NOW.month))

    def do_clear(self, args):
        sys.stdout.write("\x1b[2J\x1b[H")

    def do_eval(self, args):
        """ Evaluate `args` as Python code. """
        try:
            print (eval(args))
        except:
            try:
                print(run(args))
            except:
                print_exc()

    def do_EOF(self, args):
        return True

    def do_dump(self, args):
        """ Display all the informaion that can be obtained about the variable
            named as the first word of `args`. Some indentation would be nice.
        """
        try:
            # level = 0
            # indent = ' '*level
            # subject = globals()[args.split()[0]]
            subject = eval(args.split()[0])
            pprint(subject)
            print(str(type(subject)))
            # UNDER CONSTRUCTION
            # dump(subject)
        except KeyError:
            print_exc()

    def default(self, args):
        self.do_eval(args)

    def do_ls(self, args):
        ls(shlex.split(args))

if __name__ == "__main__":
    print(f"Testing {__file__}...")
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
