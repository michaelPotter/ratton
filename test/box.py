#!/usr/bin/env python3
#
# box.py
#
# Michael Potter
# 2020-10-07

from ratton.lib.models import Box, Point

def test_width_height():
    b1 = Box(Point(0,0), Point(4,4))
    assert b1.width == 5
    assert b1.height == 5

    b2 = Box(Point(3,7), Point(8,11))
    assert b2.width == 6
    assert b2.height == 5


    b3 = Box(Point(0,0), width=4, height=5)
    assert b3.end.x == 3
    assert b3.end.y == 4



def test_offset():
    # I'm intentionally not going to test if a larger box gets offset into a
    # smaller box because that behavior might change in the future

    def test_overlap_on_0():
        b1 = Box(Point(0,0), Point(4,4))
        b2 = Box(Point(0,0), Point(4,4))
        b3 = b1.offset(b2)
        assert b3 == b1 # should be the same really

        b4 = Box(Point(0,0), Point(2,2))
        b5 = b1.offset(b4)
        assert b4 == b5

    def test_offset1():
        b1 = Box(Point(0,0), Point(4,4))
        b2 = Box(Point(1,1), Point(2,2))
        b3 = b1.offset(b2)
        assert b3.x == 1
        assert b3.y == 1
        assert b3.end == (2,2)

    def test_offset2():
        b1 = Box(Point(2,3), Point(10,10))
        b2 = Box(Point(1,1), Point(2,2))
        b3 = b1.offset(b2)
        assert b3.x == 3
        assert b3.y == 4
        assert b3.end == (4,5)

    test_overlap_on_0()
    test_offset1()
    test_offset2()

def test_equality():
    # sanity check to make sure __eq__ works
    b1 = Box(Point(0,0), Point(4,4))
    b2 = Box(Point(0,0), Point(4,4))
    assert b1 == b2

if __name__ == "__main__":
    test_width_height()
    test_equality()
    test_offset()
    print("you should have seen no output")
