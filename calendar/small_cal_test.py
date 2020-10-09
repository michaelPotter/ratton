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

from enum import Enum

# Set up some constants
day_width = 10

sun = Point(9, 1)
mon = Point(19, 1)
tue = Point(29, 1)
wed = Point(39, 1)
thu = Point(49, 1)
fri = Point(59, 1)
sat = Point(69, 1)

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        pager_border = Box(Point(2,0), width=82, height=26)
        shapes.box(pager_border, "fancy")

        current_time()
        print_times()
        print_days()
        sample_events()

        ticker = Ticker("Events w/ long text could scroll (11-11:30am)", Box(Point(mon.x,7), width=day_width, height=1))

        # # line numbers
        # for i in range(1,24):
        #     printat(0,i,i)

        while True:
            ticker.render()
            ticker.tick()
            key = term.inkey(timeout=0.3)
            if key == 'q':
                exit()


def current_time():
    low='▁'
    mid='─'
    high='▔'
    heavy='━'
    tri='▶'
    ltri='◀'

    attr="red_on_black"

    # full week
    shapes.hline(9, 13, 82 - 8, mid, attr)

    # wed, 1:30
    shapes.hline(wed.x-1, 12, 11, heavy, attr)
    # printat(wed.x-1, 12, tri, attr)
    # printat(thu.x-1, 12, ltri, attr)

    # wed, 11:30
    shapes.hline(wed.x-1, 8, 11, mid, attr)
    printat(wed.x-1, 8, tri, attr)
    printat(thu.x-1, 8, ltri, attr)


def print_times():
    i = 3
    for h in [ y for x in [range(9,13), range(1,8)] for y in x ]:
        for m in [ "00", "30" ]:
            printat(3, i, (f"{h:02}:{m}"))
            # hour lines
            # if i%2 == 1:
            #     shapes.hline(8, i, 82 - 9, '`')
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
    w = day_width
    w = 9

    def event_text(x, y, t, attr="black_on_magenta"):
        t = t[:w]
        printat(x, y, getattr(term, attr)(t))

    # Standup(s)
    for i in [mon.x, tue.x, wed.x, fri.x]:
        event_text(i, 4, "Standup   ")
    event_text(wed.x, 4, "Standup   ", "magenta_on_black")
    # printat(thu.x, 3, term.underline(term.magenta_on_black("    ▁▁▁▁▁")))
    printat(thu.x, 4, term.underline(term.magenta_on_black("Standup  ")))

    # mon, 1-2:30, sprint review
    color_block("magenta", Box(Point(mon.x, 11), width=w, height=3))
    event_text(mon.x, 11, "Sprint Re")
    event_text(mon.x, 12, "view/Ret..")
    event_text(mon.x, 13, "1-2:30pm")

    # tue, 1-4, sprint planning
    color_block("magenta", Box(Point(tue.x, 11), width=w, height=6))
    event_text(tue.x, 11, "Sprint")
    event_text(tue.x, 12, "Planning")
    event_text(tue.x, 13, "1-4pm")

    # wed, 1-4, sprint planning
    color_block("black", Box(Point(wed.x, 11), width=w, height=6))
    shapes.box(Box(Point(wed.x, 11), width=w, height=6), "outer", attr="magenta")
    event_text(wed.x+1, 12, "Testing", "magenta_on_black")
    event_text(wed.x+1, 13, "other ", "magenta_on_black")
    event_text(wed.x+1, 14, "designs", "magenta_on_black")
    event_text(wed.x+1, 15, "1-4pm", "magenta_on_black")

    # thu, 1-4, sprint planning
    color_block("black", Box(Point(thu.x, 11), width=w, height=6))
    shapes.box(Box(Point(thu.x, 11), width=w, height=6), "fancy", attr="magenta")
    event_text(thu.x+1, 12, "Line ch", "magenta_on_black")
    event_text(thu.x+1, 13, "ars are", "magenta_on_black")
    event_text(thu.x+1, 14, "ok but", "magenta_on_black")
    event_text(thu.x+1, 15, "shrink", "magenta_on_black")
    event_text(thu.x+3, 16, "box", "magenta_on_black")

    # fri, 1-4, sprint planning
    color_block("black", Box(Point(fri.x, 11), width=w, height=6))
    shapes.box(Box(Point(fri.x, 11), width=w, height=6), "eighth", attr="magenta")
    event_text(fri.x+1, 12, "I like", "magenta_on_black")
    event_text(fri.x+1, 13, "this but", "magenta_on_black")
    event_text(fri.x+1, 14, "not the", "magenta_on_black")
    event_text(fri.x+1, 15, "corners", "magenta_on_black")

    # eighth_charset = Charset('▔', '▕', '▁', '▏', '╲', '╱', '╲', '╱')
    printat(fri.x, 5, "▁"*9, "magenta_on_black")
    printat(fri.x-1, 6, "▕this ones▏", "magenta_on_black")
    printat(fri.x-1, 7, "▕fudgy    ▏", "magenta_on_black")
    printat(fri.x, 8, "▔"*9, "magenta_on_black")

    # sat, 1-4, sprint planning
    lt='░'
    md='▒'
    drk='▓'
    color_block("magenta", Box(Point(sat.x, 11), width=w, height=6), char=lt, reverse=False)
    event_text(sat.x, 11, "Sprint")
    event_text(sat.x, 12, "Planning")
    event_text(sat.x, 13, "1-4pm")


    # Testing higher resolution event sizes
    lowerblocks = ["", "▁", "▂", "▃", "▄", "▅", "▆", "▇"]
    # mon, 6-7, test
    x=sun.x
    color_block("green", Box(Point(x, 21), width=w, height=2))

    for i in range(1,7):
        x=sun.x + day_width*i
        color_block("green", Box(Point(x, 21), width=w, height=2))
        printat(x, 23, term.black_on_green(lowerblocks[8-i])*w)
    printat(sun.x, 19, term.webgray("# There are block chars in 1/8 size increments we can use for finer"))
    printat(sun.x, 20, term.webgray("# resolution event boxes:"))

    

def color_block(color, box, char=' ', reverse=True):
    if reverse:
        attr = f"black_on_{color}"
    else:
        attr = color
    for i in range(box.height):
        printat(box.start.x, box.start.y + i, getattr(term, attr)(char * box.width))


class Ticker():
    """ PoC ticker class """
    def __init__(self, text, box):
        self.text = text
        self.box = box
        self._tick = -5 # less than 0 means don't start scrolling right away

    def tick(self):
        self._tick += 1
        if self._tick > len(self.text) + 4:
            self._tick = -5

    def render(self):
        i = max(0, self._tick)
        end = i + self.box.width
        text = f"{self.text[i:end]:{self.box.width}}"
        printat(self.box.start.x, self.box.start.y, text, "black_on_blue")



if __name__ == "__main__":
    main()
