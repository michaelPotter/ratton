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

    pager_border = Box(Point(0,1), width=term.width, height=13)
    pager_box = Box(Point(1,2), width=term.width - 2, height=11)
    pager = linepager.LinePager(pager_box, text)

    with term.fullscreen(), term.cbreak():
        pager.draw()
        pager.focus()
        shapes.box(pager_border)
        while True:
            key = term.inkey()
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
            elif key == 'g':
                key2 = term.inkey(timeout=1)
                if key2 == 'g':
                    pager.scroll_top()


def demo():
    print(term.home + term.clear + term.move_y(term.height // 2))
    print(term.black_on_darkkhaki(term.center('press any key to continue')))


    with term.cbreak(), term.hidden_cursor():
        inp = term.inkey()

    print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))

if __name__ == "__main__":
    main()
