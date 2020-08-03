from math import *
from mecode import G
import numpy as np
import pandas as pd
# from sympy import *

SAFETY_LINE = "G90 G80 G40 G17 G00"

Tool = namedtuple("Tool", ["type", "diameter", "teeth"])

TOOLS = [Tool('drill', 0.15, 3), Tool('drill', 0.221, 3), Tool('drill', 1.275, 3),
         Tool('mill', 0.25, 3),  Tool('center', 0.125, 2)]

SURFACE_SPEED = 150
CHIP_LOAD = 0.005

ORIGIN = [0.0] * 3

def capture_output(f):
    def g(*args, **kwargs):
        cout = sys.stdout
        sys.stdout = StringIO()
        f(*args, **kwargs)
        value = sys.stdout.getvalue()
        sys.stdout = cout
        return value
    return g

@capture_output
def tool(n):
    T = None
    i = 0
    if type(n) is int:
        i = n-1
        T = TOOLS[i]
    else:
        for j, t in enumerate(TOOLS):
            if t.diameter == n:
                T = t
                i = j
    if not T: T = Tool("none", "0.0", 0)
    # print(T)
    # print(T.diameter)
    speed = int(round((SURFACE_SPEED * 12) / (pi * T.diameter)))
    # print(speed)
    feed = round(speed * CHIP_LOAD * T.teeth, 4)
    # print(feed)
    print(f"""G91 G30 Z0.0 Y0.0 ;
T{i+1} M6 ;
S{speed} F{feed} M3 ;
""")


def pt2gstr(point):
    value = str()
    codes = ['X','Y','MZ']
    for i, (x, x0) in enumerate(zip(point, pt2gstr.position)):
        if x != x0:
            value += codes[i] + str(round(x, 4)) + ' '
    pt2gstr.position = point
    return value

pt2gstr.__setattr__('position', ORIGIN)
pt2gstr.position

@capture_output
def drilling_cycle(points, ret=0.2):
    print(f"G99 G81 {pt2gstr(points[0])}R{ret}")
    for p in points[1:]:
        print(pt2gstr(p))

g = G()
g.output_digits = 4
absolute = g.absolute

def rapid(P):
    g.abs_rapid(*P)

def move(P):
    g.abs_move(*P)

def arc(P, r):
    g.abs_arc(x=P[0], y=P[1], radius=r)

def ccw(P, r):
    g.abs_arc(x=P[0], y=P[1], radius=r, direction='CCW')

def edit(s):
    current_x = Q[0][0]
    current_y = Q[0][1]
    current_z = SAFE_Z
    ABS_POS = 90
    REL_POS = 91
    RAPID_MOVE = 0
    CUT_MOVE = 1
    ARC_MOVE = 2
    CCW_MOVE = 3
    current_pos_mode = REL_POS
    current_move_mode = RAPID_MOVE
    MOVE_CODES = list(range(3))
    POS_CODES = [90, 91]

    words = list()
    for i, s in enumerate(s):
        if s:
            block = list()
            for j, w in enumerate(s.split(' ')):
                mark4del = False
                CMD = w[0]
                CODE = (int if CMD == 'G' else float)(w[1:])
#                 print(f"{CMD=} {CODE=}")
                if CMD == 'G':
                    if CODE in MOVE_CODES:
                        if CODE != current_move_mode:
                            current_move_mode = CODE
                        else:
                            mark4del = True
                    elif CODE in POS_CODES:
                        if CODE != current_pos_mode:
                            current_pos_mode = CODE
                        else:
                            mark4del = True
                elif CMD in {'X', 'x'}:
                    if CODE != current_x:
                        current_x = CODE
                    else:
                        mark4del = True
                elif CMD in {'Y', 'y'}:
                    if CODE != current_y:
                        current_y = CODE
                    else:
                        mark4del = True
                elif CMD in {'Z', 'z'}:
                    if CODE != current_z:
                        current_z = CODE
                    else:
                        mark4del = True

                if not mark4del:
                    block.append(w.rstrip('0'))

            words.append(' '.join(block))

    return ' ;\n'.join(words) + ' ;\n'
