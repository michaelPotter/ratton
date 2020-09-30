#!/usr/bin/env python3
#
# pager.py
#
# Michael Potter
# 2020-07-15

from util import *

class Pager(object):
    """
    Renders a pager of content on a subsection of the screen
    Allows scrolling through the content
    This displays the text, but doesn't handle any cursor actions.

    important attributes:

    box: this is the bounding box that the pager can display in
    text: the buffer of text this pager is paging
    pos: the lineno of the first line of text the pager is currently
        displaying. may not go above len(text) - box.height
    apos: this is the lineno of the _last_ line of text the pager is
        displaying.
    """
    # TODO this first! add function for getting the nth line of text
    # TODO: implement side scrolling
    # TODO implement page-by-page scrolling
    def __init__(self, box, text):
        super(Pager, self).__init__()
        self.box = box
        self.text = Buffer(text)
        self.pos = 0

        if len(self.text) == 0:
            raise Exception("pager input length is 0")

    def draw(self):
        with term.location(*self.box.start):
            text = self.text.getLines(self.pos, self.height)
            # truncate & print each line
            for y,line in enumerate(text, self.y):
                line = line[:self.width]
                p(term.move_xy(self.x, y) + line.ljust(self.width))

    def scroll_up(self, n=1):
        """ scroll the pager up one line """
        if self.pos > 0:
            self.pos -= 1
            self.draw()

    def scroll_down(self, n=1):
        """ scroll the pager down one line """
        if self.pos < len(self.text) - self.height:
            self.pos += 1
            self.draw()

    def scroll_bottom(self):
        self.pos = len(self.text) - self.height
        self.draw()

    def scroll_top(self):
        self.pos = 0
        self.draw()

    def get_line(self, n):
        """
        Return the nth line of the pager
        return the empty string if n is out of bounds
        """
        return self.text.getLines(self.pos + n, 1)[0]

    def trim_line(self, n):
        """
        Return the nth line of the pager, trimmed to fit the screen
        return the empty string if n is out of bounds
        """
        line = self.get_line(n)[:self.width]
        return f'{line:{self.width}}'

    def repaint_line(self, n, attr):
        """
        Repaints line n with the given text attribute
        attr can be any text attr that term takes.
        For example you could repaint line 4 with "bold_blink_red_on_green"
        """
        printat(self.x, self.y + n, getattr(term, attr)(self.trim_line(n)))

    @property
    def apos(self):
        return self.pos + self.height - 1

    @property
    def width(self):
        return self.box.width

    @property
    def height(self):
        return self.box.height

    @property
    def x(self):
        return self.box.x

    @property
    def y(self):
        return self.box.y



class Buffer(object):
    """Class for holding the text of the pager"""
    def __init__(self, text):
        super(Buffer, self).__init__()
        self.text = text.splitlines()

    def getLines(self, start, n):
        return self.text[start:start + n]

    def __len__(self):
        return len(self.text)

