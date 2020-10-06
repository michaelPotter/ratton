#!/usr/bin/env python3
#
# keysink.py
#
# Michael Potter
# 2020-10-05


class MultiKeysink(object):

    """
    A keysink is a function that takes a key and performs some operation based
    on which key was given. A MultiKeysink is a collection of keysinks that
    will each be tried until the key is handled.

    If a keysink didn't handle a key, it should return False to signal that the
    next keysink should be tried.

    When multiple keysinks can handle the same key, the most recently added sink
    will succeed, and earlier sinks won't be tried.
    """

    def __init__(self):
        self.keysinks = []

    def add(self, keysink):
        self.keysinks.insert(0, keysink)

    def apply(self, key):
        """
        Keep applying keysinks until one doesn't return false
        """
        for k in self.keysinks:
            if (k(key) != False):
                break
        

def get_pager_keysink(pager):
    """
    Returns a keysink that handles many vim-like actions on the given pager
    """

    def sink(key):
        if key == 'j':
            pager.down()
        elif key == 'k':
            pager.up()
        elif key == 'h':
            p(term.move_left(1))
        elif key == 'l':
            p(term.move_right(1))
        elif key == 'g':
            key2 = term.inkey(timeout=1)
            if key2 == 'g':
                pager.goto_line(0)
        elif key == 'G':
            pager.goto_line('$')
        elif key == 'L':
            pager.bottom_line()
        elif key == 'H':
            pager.top_line()
        elif key == 'M':
            pager.middle_line()
        else:
            return False

    return sink
