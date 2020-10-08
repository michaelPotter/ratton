#!/usr/bin/env python3
#
# models.py
#
# Michael Potter
# 2020-07-16

from collections import namedtuple

Point = namedtuple('Point', ('x', 'y'))

class Box(object):
    """
    Contains bounding info between two points on the screen

    @param start: a Point showing where to start the box
    @param end: an optional Point showing where to end the box. The box is
        inclusive of this point, e.g. if start.x is 2 and end.x is 4, the width
        will be 3
    @param width: The width of the box. Required if 'end' is not provided
    @param height: The height of the box. Required if 'end' is not provided

    """
    def __init__(self, start, end=None, width=None, height=None):
        super(Box, self).__init__()

        # make sure we have either and end or a width and height
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

    def offset(self, other):
        """
        Takes another box, and creates a new box that is the offset of the
        other box within this one.

        Currently, if the inner box overlaps outside the outer box, no
        truncation is done. Maybe I'll add a flag or something for that later.

        e.g. if you run:
            b1 = Box(Point(5,4), width=10, height=7)
            b2 = Box(Point(4,1), width=4, height=3)
            b3 = b1.offset(b2)
        b3 will be equivalent to Box(Point(9, 5), width=4, height=3)


            0    5    10   15
            v    v    v    v
         0 >     .    .
                +--+  .
                |b2|  .
                +--+  .
                 +---------+
         5->     |b1 +--+  |
                 |   |b3|  |
                 |   +--+  |
                 |         |
                 |         |
        10->     +---------+
        """
        if other is None:
            return None

        return Box(
                Point(
                    self.start.x + other.start.x,
                    self.start.y + other.start.y),
                width = other.width,
                height = other.height)

    def bound_outer(self):
        """
        Returns a box bigger than this one by a value of 1 on all sides. Useful
        for creating a border.
        For example, given box = Box(Point(1,1), Point(4,4)), box.bound_outer()
        will return a box equivalent to Box(Point(0,0), Point(5,5)).
        """
        return Box(
                Point(self.start.x - 1, self.start.y - 1),
                Point(self.end.x + 1, self.end.y + 1))

    def bound_inner(self):
        """
        Like Box.bound_outer(), but returns a box smaller by 1 on all sides.
        For example, given box = Box(Point(1,1), Point(4,4)), box.bound_inner()
        will return a box equivalent to Box(Point(2,2), Point(3,3)).
        """
        return Box(
                Point(self.start.x + 1, self.start.y + 1),
                Point(self.end.x - 1, self.end.y - 1))

    def __repr__(self):
        return f'Box([{self.x}, {self.y}]-[{self.end.x}, {self.end.y}], w={self.width}, h={self.height})'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if other == None:
            return False
        return self.start == other.start and self.end == other.end


