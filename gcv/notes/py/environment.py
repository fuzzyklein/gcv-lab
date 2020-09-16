from collections import ChainMap
from configparser import ConfigParser
from enum import Enum
import logging
from pprint import pformat, pprint as pp

from sympy import Point3D
Point = Point3D


from sympy import Point3D
Point = Point3D

DEFAULT_GCODES = [ list(), MotionMode.RAPID, CircularPlane.XY, PositionMode.ABSOLUTE, FeedMode.PER_MINUTE,
                   Units.INCHES, CutterOffsetMode.OFF, ToolOffsetMode.NEGATIVE, CannedCycle.CANCEL,
                   ReturnMode.INITIAL_POINT, False, 54, ExactStopModal.OFF, False ]

DEFAULT_VARS = {
#     "current_position" : Point(),
    "A" : 0.0,
    "B" : 0.0,
    "C" : 0.0,
    "D" : 0,
    "E" : 0.0001, # minimum; 0.25 is the max
    "F" : 0.0,
    'G' : dict(zip(gCodeClassList, DEFAULT_GCODES)),
    'H' : 0,
    "I" : 0.0,
    "J" : 0.0,
    "K" : 0.0,
    "L" : 0.0,
    "M" : None,
    "N" : None,
    "O" : 0,
    "P" : 0.0,
    "Q" : 0.0,
    "R" : 0.0,
    "S" : 1,
    "T" : 0,
    "U" : 0.0001,
    "V" : 0.0001,
    "W" : 0.0001,
    "X" : 0.0,
    "Y" : 0.0,
    "Z" : 0.0,

}


class Environment(ChainMap):
    WORK_COORDS_RANGE = [ *range(53,60), *range(110, 130) ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
logging.debug(f"{__name__} module loaded")

