from configparser import ConfigParser
from enum import Enum
from functools import reduce
import logging
from operator import and_
from pathlib import Path
import string
import sys


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
                    if not self[-1].validate():
                        raise Exception(f"ERROR: Invalid command: {self[-1]}")

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

    def __init__(self, lines=list()):
        super(list, self).__init__()
        if type(lines) is str:
            lines = lines.split(NEWLINE)
        for line in lines:
            self.append(Block(line))
        self.current_block = 0
        self._state = 0

    # def run(self):
    #     while self.state != self.State.END:
    #         self.step()

    def step(self):
        """
        """
        if self.current_block >= len(self):
            self.state = self.State.END
        else:
            i = self.current_block
            self.current_block += 1
            return self[i].execute()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, n):
        self._state = n




