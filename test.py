#!/usr/bin/env python3
#
# test.py
#
# Michael Potter
# 2020-07-15

from blessed import Terminal

from pager import Pager
import linepager
from models import *
from util import *
import shapes

def main():
    with open('ls.txt') as f:
        text = f.read()

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
        pager.scroll_bottom()
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
            pager.scroll_top()


def cmd_line_mode():
    with term.location(0, term.height-1), term.cbreak():

        # this erases the whole line
        p(':'.ljust(term.width))

        # so move back to the first char
        p(term.move_xy(1, term.height-1))
        
        # get the input command
        cmd = ""
        while True:
            key = term.inkey()
            if key.code == term.KEY_ENTER:
                break
            cmd += key
            p(key)

def demo():
    print(term.home + term.clear + term.move_y(term.height // 2))
    print(term.black_on_darkkhaki(term.center('press any key to continue')))


    with term.cbreak(), term.hidden_cursor():
        inp = term.inkey()

    print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))

if __name__ == "__main__":
    main()
