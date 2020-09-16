from configparser import ConfigParser
from enum import Enum, IntEnum
import logging
from pathlib import Path
import sys

WorkCoordinates = int

class NonModal(IntEnum):
    DWELL = 4
    EXACT_STOP = 9
    SET_OFFSETS = 10
    CLOCKWISE_CIRCULAR_POCKET_MILLING = 12
    COUNTER_CLOCKWISE_CIRCULAR_POCKET_MILLING = 13
    RETURN_2_REF_PT = 28
    SET_RETURN_THRU_REF_PT = 29
    FEED_UNTIL_SKIP = 31 # optional
    AUTO_TOOL_DIAMETER_MEASURE = 35 # optional
    AUTO_WORK_OFFSET_MEASURE = 36 # optional
    AUTO_TOOL_OFFSET_MEASURE = 37 # optional
    TEXT_ENGRAVING = 47
    SET_LOCAL_SHIFT_COORDINATE_SYSTEM = 52 # fanuc
    NON_MODAL_MACHINE_COORDINATE_SELECTION = 53
    UNIDIRECTIONAL_POSITIONING = 60
    MACRO_SUBROUTINE_CALL = 65 # optional
    BOLT_HOLE_CIRCLE = 70 # yasnac
    BOLT_HOLE_ARC = 71 # yasnac
    BOLT_HOLES_ANGLE = 72
    SET_WORK_COORDINATES = 92
    CANCEL_MIRROR_IMAGE = 100
    ENABLE_MIRROR_IMAGE = 101
    PROGRAMMABLE_OUTPUT = 102
    LIMIT_BLOCK_BUFFERING = 103
    CYLINDRICAL_MAPPING = 107
    AUTOMATIC_WORK_OFFSET_CENTER_MEASURE = 136
    GENERAL_PURPOSE_POCKET_MILLING = 150
    SPECIAL_PURPOSE_RIGID_TAPPING_COUNTER_CLOCKWISE = 174
    SPECIAL_PURPOSE_RIGID_TAPPING_CLOCKWISE = 184
    ACCURACY_CONTROL = 187

class MotionMode(IntEnum):
    RAPID = 0
    LINEAR = 1
    CLOCKWISE = 2
    COUNTER = 3
    # POCKET = 12
    # COUNTER_POCKET = 13

class PositionMode(IntEnum):
    ABSOLUTE = 90
    INCREMENTAL = 91

class CutterOffsetMode(IntEnum):
    OFF   = 40
    LEFT  = 41
    RIGHT = 42

class CannedCycle(IntEnum):
    NONE = 0
    CANCEL = 80
    DRILL = 81
    SPOT = 82
    PECK = 83
    TAP = 84
    BORE = 85
    IN_OUT = 86
    RETRACT = 87
    MANUAL = 88
    DWELL = 89

class CircularPlane(IntEnum):
    XY = 17
    ZX = 18
    YZ = 19

class Units(IntEnum):
    INCHES = 20
    METRIC = 21

class ToolOffsetMode(IntEnum):
    POSITIVE = 43
    NEGATIVE = 44
    OFF = 49

class ExactStopModal(IntEnum):
    ON = 61
    OFF = 64

class FeedMode(IntEnum):
    INVERSE_TIME = 93
    PER_MINUTE = 94

class ReturnMode(IntEnum):
    INITIAL_POINT = 98
    R_PLANE = 99

class MirrorImage(IntEnum):
    CANCEL = 100
    ENABLE = 101

class SpindleState(IntEnum):
    OFF = 0
    FORWARD = 1
    REVERSE = 2

class ScalingMode(IntEnum):
    OFF = 50
    ON = 51

class Rotation(IntEnum):
    ON = 68
    OFF = 69

class GCodeGroup(Enum):
    NON_MODAL = NonModal
    MOTION = MotionMode
    PLANE = CircularPlane
    POSITION_MODE = PositionMode
    FEED_MODE = FeedMode
    UNITS = Units
    CUTTER_COMPENSATION = CutterOffsetMode
    TOOL_LENGTH = ToolOffsetMode
    CANNED_CYCLE = CannedCycle
    RETURN = ReturnMode
    SCALING = ScalingMode
    WORK_COORDINATES = WorkCoordinates
    EXACT_STOP_MODAL = ExactStopModal
    ROTATION = Rotation

gCodeClassList = [
    NonModal, MotionMode, CircularPlane, PositionMode, FeedMode, Units, CutterOffsetMode, ToolOffsetMode,
    CannedCycle, ReturnMode, ScalingMode, WorkCoordinates, ExactStopModal, Rotation
]

gCodeGroups = {
    GCodeGroup.NON_MODAL : [ 4, 9, 10, 12, 13, 28, 29, 32, *range(35, 38),
                             47, 52, 53, 60, 65, *range(70, 73), 92,
                             *range(100, 104), 107, 136, 150, 174, 184, 187
                           ],
    GCodeGroup.MOTION : [ *range(0, 4), ],
    GCodeGroup.PLANE : [ *range(17, 20)],
    GCodeGroup.POSITION_MODE : [ 90, 91 ],
    GCodeGroup.FEED_MODE : [ 93, 94 ],
    GCodeGroup.UNITS : [ 20, 21 ],
    GCodeGroup.CUTTER_COMPENSATION : [ *range(40, 43), 141 ],
    GCodeGroup.TOOL_LENGTH : [ 43, 44, 49, 143 ],
    GCodeGroup.CANNED_CYCLE : [ *range(73, 90) ],
    GCodeGroup.RETURN : [ 98, 99 ],
    GCodeGroup.SCALING : [ 50, 51 ],
    GCodeGroup.WORK_COORDINATES : [ *range(54, 60), *range(100, 130) ],
    GCodeGroup.EXACT_STOP_MODAL : [ 61, 64 ],
    GCodeGroup.ROTATION : [ 68, 69 ]
}

gCodeGroupsDict = dict(zip(gCodeGroups.keys(), gCodeClassList))



