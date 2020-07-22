#!/usr/bin/env python3
#
# util.py
#
# Michael Potter
# 2020-07-16

from functools import partial
from blessed import Terminal

# Note that by importing as `from util import *` any importing modules will get
# this term instance too
term = Terminal()

p = partial(print, end='', flush=True)

def printat(x, y, s):
    with term.location(x,y):
        p(s)
