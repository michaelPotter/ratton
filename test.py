#!/usr/bin/env python3
#
# test.py
#
# Michael Potter
# 2020-07-15

from blessed import Terminal

import os.path
from pager import Pager
import linepager
from models import *
from util import *
import shapes
import readline
import subprocess


def pager_mode_keysink(key, pager):
    if key == 'q':
        exit()
    elif key == 'j':
        # p(term.move_down(1))
        pager.down()
    elif key == 'k':
        # p(term.move_up(1))
        pager.up()
    elif key == 'h':
        p(term.move_left(1))
    elif key == 'l':
        p(term.move_right(1))
    elif key == 'G':
        pager.goto_line('$')
    elif key == 'L':
        pager.bottom_line()
    elif key == 'H':
        pager.top_line()
    elif key == 'M':
        pager.middle_line()
    elif key == ':':
        global mode
        mode = "cmdline"
    elif key == 'g':
        key2 = term.inkey(timeout=1)
        if key2 == 'g':
            pager.goto_line(0)


def cmd_line_mode():
    with term.location(0, term.height-1):

        cmd = input(":")

        pager.draw()
        if cmd.strip() == "q":
            exit()




if __name__ == "__main__":
    proc = subprocess.run(["ls", "-al", os.path.expanduser("~")], capture_output=True)
    text = proc.stdout.decode('utf-8')

    pager_box = Box(Point(0,0), width=term.width, height=term.height-1 )
    pager = linepager.LinePager(pager_box, text)

    with term.fullscreen():
        global mode
        mode = "pager"
        pager.draw()
        pager.focus()
        while True:
            if mode == "pager":
                with term.cbreak():
                    key = term.inkey()
                    pager_mode_keysink(key, pager)
            elif mode == "cmdline":
                cmd_line_mode()
                mode = "pager"
