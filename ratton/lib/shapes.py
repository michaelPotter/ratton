#!/usr/bin/env python3
#
# shapes.py
#
# Michael Potter
# 2020-07-16

from ratton.lib.util import *
from collections import namedtuple

def vline(x, y, height, char='|', attr=None):
    if attr:
        char = getattr(term, attr)(char)
    with term.location(x, y):
        for yy in range(y, y + height):
            p(term.move_xy(x, yy) + char)

def hline(x, y, width, char='-', attr=None):
    if attr:
        char = getattr(term, attr)(char)
    with term.location(x, y):
        for xx in range(x, x + width):
            p(term.move_xy(xx, y) + char)

def box(box, charset="ascii", attr=None):
    """ Draws a box outline """
    Charset = namedtuple('Charset', (
        'n_walls', 'e_walls', 's_walls', 'w_walls',
        'ne_corner', 'se_corner', 'sw_corner', 'nw_corner'))
    ascii_charset = Charset('-', '|', '-', '|', '+', '+', '+', '+')
    fancy_charset = Charset('─', '│', '─', '│', '┐', '┘', '└', '┌')
    outer_charset = Charset('▀', '▐', '▄', '▌', '▜', '▟', '▙', '▛')
    eighth_charset = Charset('▔', '▕', '▁', '▏', '╲', '╱', '╲', '╱')

    if charset == "ascii":
        c = ascii_charset
    elif charset == "fancy":
        c = fancy_charset
    elif charset == "outer":
        c = outer_charset
    elif charset == "eighth":
        c = eighth_charset


    # add attributes to each item
    if attr:
        c = Charset(*[ getattr(term, attr)(a) for a in c ])

    with term.location(*box.start):
        p(c.nw_corner)
        p(term.move_xy(box.start.x, box.end.y) + c.sw_corner)
        p(term.move_xy(box.end.x, box.start.y) + c.ne_corner)
        p(term.move_xy(*box.end) + c.se_corner)
        hline(box.start.x + 1, box.start.y, box.width - 2, c.n_walls)
        hline(box.start.x + 1, box.end.y, box.width - 2, c.s_walls)
        vline(box.start.x, box.start.y + 1, box.height - 2, c.w_walls)
        vline(box.end.x, box.start.y + 1, box.height - 2, c.e_walls)

def color_block(color, box):
    """
    Draws a blank block filled with a given color in the given bounding box.
    If you're going to write text on top of this, you'll have to set the
    background color of the text manually.
    """
    for i in range(box.height):
        printat(box.start.x, box.start.y + i, getattr(term, f"black_on_{color}")(' ' * box.width))
