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

    important attributes:

    line: this is the highlighted line on the page. Must be between 0 and
        pager height. 0 means the top line that is currently displayed by the
        pager, not the 0th line of text.
    """
    def __init__(self, box, text):
        super(LinePager, self).__init__(box, text)
        self.line = 0
        
    def draw(self):
        super().draw()
        self.draw_cursorline()

    def draw_cursorline(self):
        self.repaint_line(self.line, "reverse")

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

    def goto_line(self, n):
        """
        move the cursor to the nth line of the buffer
        pass in '$' or -1 to go to the last line
        """
        if type(n) is str:
            if n.startswith('$'):
                if n == '$':
                    dst = len(self.text) - 1
                else:
                    offset = n[1:]
                    dst = len(self.text) + int(offset)
            else:
                # TODO invalid
                return
        else:
            dst = n

        if dst < 0 or dst >= len(self.text):
            # invalid position
            return

        if dst < self.pos:
            # if we need to scroll backward
            self.pos = dst
            self.top_line()
        elif dst > self.apos:
            # if we need to scroll forward
            self.pos = dst - self.height + 1
            self.bottom_line()
        else:
            self.line = dst - self.pos
            self.draw()

    def up(self, n=1):
        """ move the cursor up """
        if self.line > 0:
            self.line -= 1
            p(term.move_up(1))
            self.draw()
        else:
            self.scroll_up()

    def down(self, n=1):
        """ move the cursor down """
        if self.line < self.box.height - 1:
            self.line += 1
            p(term.move_down(1))
            self.draw()
        else:
            self.scroll_down()

    def top_line(self):
        """ select the top visible line of the pager """
        p(term.move_y(self.y))
        self.line = 0
        self.draw()

    def bottom_line(self):
        """ select the bottom visible line of the pager """
        self.line = self.height - 1
        p(term.move_y(self.y + self.line))
        self.draw()

    def middle_line(self):
        """ select the line in the middle of the pager """
        self.line = self.height // 2
        p(term.move_y(self.y + self.line))
        self.draw()

    def get_focused(self):
        """ return the currently focused line """
        return self.get_line(self.line)
