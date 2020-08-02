#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-
""" setup.py
    v1.0.0c

    Installer script for the cleandir command line script.

    Copyright &copy; 2018 by Russell Klein. All rights reserved.

    This script uses the `setuptools` module to install the `python` script
    defined by the files contained within this directory. As such it requires
    direct modification in order to produce a useful program with it.
    The `setup` function takes care of everything according to its keyword
    arguments, so it's really just a matter of setting those properly.
"""

from setuptools import find_packages, setup

PROGRAM_NAME = "cleandir"

ENTRY_POINTS = { "console_scripts" : "{} = {}.{}:main".format(PROGRAM_NAME,
                                                              PROGRAM_NAME,
                                                              PROGRAM_NAME
                                                             )
               }

config = {
    'description': PROGRAM_NAME,
    'version': "1.0.0c",
    'name': PROGRAM_NAME,
    'entry_points': ENTRY_POINTS,
    'packages': find_packages(include=(PROGRAM_NAME, PROGRAM_NAME+".*"))
}

if __name__ == "__main__":
    # config["packages"] = find_packages(include=(PROGRAM_NAME, PROGRAM_NAME+".*"))
    setup(**config)
