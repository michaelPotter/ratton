#!/usr/bin/env python3
#
# shapes.py
#
# Michael Potter
# 2020-07-16

from util import *

def vline(x, y, height):
    with term.location(x, y):
        for yy in range(y, y + height):
            p(term.move_xy(x, yy) + '|')

def hline(x, y, width):
    with term.location(x, y):
        for xx in range(x, x + width):
            p(term.move_xy(xx, y) + '-')

def box(box):
    with term.location(*box.start):
        p('+')
        p(term.move_xy(box.start.x, box.end.y) + '+')
        p(term.move_xy(box.end.x, box.start.y) + '+')
        p(term.move_xy(*box.end) + '+')
        hline(box.start.x + 1, box.start.y, box.width - 2)
        hline(box.start.x + 1, box.end.y, box.width - 2)
        vline(box.start.x, box.start.y + 1, box.height - 2)
        vline(box.end.x, box.start.y + 1, box.height - 2)
