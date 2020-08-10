from cmd import Cmd
import re

def columnize(s):
    """ Print the contents of the list `s` in neat-looking columns. """
    if s:
        Cmd().columnize(list(s))
    else:
        print("None")

def public(obj):
    columnize([member for member in dir(obj) if not re.match('_', member)])

