#!/usr/bin/env python3
#
# models.py
#
# Michael Potter
# 2020-07-16

from collections import namedtuple

Point = namedtuple('Point', ('x', 'y'))

class Box(object):
    """Contains bounding info between two points on the screen"""
    def __init__(self, start, end=None, width=None, height=None):
        super(Box, self).__init__()
        
        assert start is not None and (
                end is not None or (
                    width is not None and height is not None))

        if end is not None:
            self.start = start
            self.end = end
            self.width = end.x - start.x + 1
            self.height = end.y - start.y + 1
        elif width is not None:
            self.start = start
            self.width = width
            self.height = height
            self.end = Point(start.x + width - 1, start.y + height - 1)

        self.x = self.start.x
        self.y = self.start.y
        
