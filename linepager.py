#!/usr/bin/env python3
#
# linepager.py
#
# Michael Potter
# 2020-07-16

from util import *
import pager

class LinePager(pager.Pager):
    """
    A pager where you can scroll line by line
    This wraps the Pager class for rendering, but also provides methods for
    moving the cursor within the pager
    """
    def __init__(self, box, text):
        super(LinePager, self).__init__(box, text)
        self.line = 0
        
    def draw(self):
        super().draw()
        self.draw_cursorline()

    def draw_cursorline(self):
        printat(self.x, self.abs_line, term.reverse(self.get_line(self.line)))

    def focus(self):
        p(term.move_xy(self.x, self.y + self.line))

    @property
    def abs_line(self):
        """
        Return the absolute y pos of the current line on the terminal
        eg if the box starts on the line 4 of the term and we're on the
        line 2 of the box, return 6
        """
        return self.y + self.line

    def up(self, n=1):
        if self.line > 0:
            self.line -= 1
            p(term.move_up(1))
            self.draw()
        else:
            self.scroll_up()

    def down(self, n=1):
        if self.line < self.box.height - 1:
            self.line += 1
            p(term.move_down(1))
            self.draw()
        else:
            self.scroll_down()

    def top_line(self):
        self.line = 0
        self.draw()

    def bottom_line(self):
        self.line = self.height - 1
        self.draw()

    def middle_line(self):
        self.line = self.height // 2
        self.draw()
