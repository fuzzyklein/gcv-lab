from configparser import ConfigParser
from enum import Enum
from functools import reduce
import logging
from operator import and_
from pathlib import Path
import string
import sys

log = logging.getLogger(__name__)
log.setLevel(logging.WARNING)
log.addHandler(logging.NullHandler())
log.debug(f"loading {__name__} module")

CONFIG_FILE = 'etc/config.ini'
CONFIG = ConfigParser()
CONFIG.read(CONFIG_FILE)
sys.path.insert(0, str(Path.home() / CONFIG["DEFAULT"]["packages_dir"]))
print( str(Path.home() / CONFIG["DEFAULT"]["packages_dir"]))

from ncv.charconsts import *

from ncv.enumerations import *

class Word(object):
    """
    """
    def __init__(self, s):
        self.cmd = s[0].upper()
        self.param = int(s[1:].rstrip(';')) if not '.' in s[1:] else float(s[1:].rstrip(';'))

    def __repr__(self):
        return self.cmd + str(self.param)

    def __str__(self):

        return self.__repr__()

    def execute(self):
        return { self.cmd : self.param }

    def validate(self):
        return self.cmd in string.ascii_letters and type(self.param) in {int, float}



PRIORITY_LIST = [ 'O', 'G', 'A', 'B', 'C', 'I', 'J', 'K', 'L', 'P', 'Q', 'X', 'Y', 'Z',
                  'H', 'D', 'E', 'F', 'R', 'S', 'T', 'U', 'V', 'W', 'M', 'N'
                ]

class Block(list):
    """
    """
    def __init__(self, line):
        super().__init__()
        for word in line.partition(SEMICOLON)[0].split():
            word = word.upper()
            for CODE in PRIORITY_LIST:
                if word[0] == CODE:
                    self.append(Word(word))

    def __repr__(self):
        """
        """
        return ' '.join([str(s) for s in self]) + ';'

    def __str__(self):
        """
        """
        return self.__repr__()

    def pop_G_codes(self):
        result = list()
        for word in self:
            if word.cmd == 'G':
                result.append(word.param)
                self.remove(word)
        return result

    def validate(self):
        return reduce(and_, [w.validate() for w in self])


    def execute(self):
        """
        """
        print("Executing block: ", self)
        result = dict()
        gcodes = list()
#         mcode = None
        for word in self:
            # TODO: Deal with G codes here (?)
            if word.cmd == 'G':
                gcodes.append(word.param)
#             elif cmd.cmd == 'M'
            else:
                result.update(word.execute())
#         if gcodes:
#             result.update({"G" : self.make_gcodes_dict(gcodes)})
        return result

    def mCode(self):
        for w in self[-1:]:
            if w.cmd == 'M':
                return w.param
        return None


class NCProgram(list):
    """
    """
    class State(Enum):
        BEGIN = 0
        PAUSED = 1
        RUNNING = 2
        END = 3

    def __init__(self, lines):
        super(list, self).__init__()
        if type(lines) is str:
            lines = lines.split(NEWLINE)
        for line in lines:
            self.append(Block(line))

    # def run(self):
    #     while self.state != self.State.END:
    #         self.step()

    def step(self):
        """
        """
        if self.current_block >= len(self):
            self.state = self.State.END
        else:
            return self[self.current_block].execute()
            self.current_block += 1


logging.debug(f"{__name__} module loaded")

if __name__ == "__main__":
    print(f"Testing {__file__}...")
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
