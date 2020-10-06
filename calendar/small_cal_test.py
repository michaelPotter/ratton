#!/usr/bin/env python3
#
# cal.py
#
# Michael Potter
# 2020-09-23
#
# I'm just messing around to see what a term-based calendar week view might
# look like. This script renders a week in an 80x24 area just to see if you can
# fit it in the smallest terminal size. It feels a little squished, but things
# can only get better in a larger terminal

from blessed import Terminal
from ratton.lib.util import *
from ratton.lib.models import *
import ratton.lib.shapes as shapes

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        pager_border = Box(Point(2,0), width=82, height=26)
        shapes.box(pager_border)

        print_times()
        print_days()
        sample_events()

        # for i in range(1,24):
        #     printat(0,i,i)

        while True:
            key = term.inkey()
            if key == 'q':
                exit()

def print_times():
    i = 3
    for h in [ y for x in [range(9,13), range(1,8)] for y in x ]:
        for m in [ "00", "30" ]:
            printat(3, i, (f"{h:02}:{m}"))
            i += 1

def print_days():
    days = [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ]
    time_col = 6
    alloc_width = ( 80 - time_col ) // 7

    for i,d in enumerate(days):
        x = i * alloc_width + time_col + 1 + 2

        # print the day name
        printat(x, 1, d.center(alloc_width))

        # # print a sample color to show day blocks
        # color = "blue" if i % 2 == 1  else "green"
        # color_block(color, Box(Point(x, 2), width=alloc_width, height=24-1))

        # debugging
        printat(0, 33 + i, f"{d}: x={x}")
    printat(0, 32, f"day width: {alloc_width}")

def sample_events():
    w = 10
    w = 9

    def event_text(x, y, t):
        t = t[:w]
        printat(x, y, getattr(term, "black_on_magenta")(t))

    # wed, 1-4, sprint planning
    color_block("magenta", Box(Point(39, 11), width=w, height=6))
    event_text(39, 11, "Sprint")
    event_text(39, 12, "Planning")
    event_text(39, 13, "1-4pm")

    # tue, 1-2:30, sprint review
    color_block("magenta", Box(Point(29, 11), width=w, height=3))
    event_text(29, 11, "Sprint Re")
    event_text(29, 12, "view/Ret..")
    event_text(29, 13, "1-2:30pm")

    for i in [19, 29, 49, 59]:
        event_text(i, 4, "Standup   ")

    

def color_block(color, box):
    for i in range(box.height):
        printat(box.start.x, box.start.y + i, getattr(term, f"black_on_{color}")(' ' * box.width))


if __name__ == "__main__":
    main()
