#!/usr/bin/env python3
#
# week.py
#
# Michael Potter
# 2020-10-12

from datetime import date, time, timedelta, datetime

from ratton.lib.util import *
from ratton.lib.models import *
import ratton.lib.shapes as shapes
import textwrap
import math
import signal

from day import *

if __name__ == "__main__":
    h=26
    box = Box(Point(60,10), width=10, height=h)
    border = box.bound_outer()
    day_events = [
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            Event(time(12, 00), time(13, 00), 'Lunch', 'green'),
            Event(time(13, 00), time(14, 00), 'Planning', 'blue'),
            Event(time(12, 30), time(13, 30), 'Collision', 'red'),
            ]
    week_events = [ day_events for i in range(7) ]

    # scale_box = Box(Point(53, 10), width=5, height=h)
    # scale = HourScale(box.height, 3, time(9))
    # hourView = HourScaleView(scale_box, scale)

    # d = DayView(box, events, scale)

    def getFullBox():
        return Box(Point(0,0), width=term.width, height=term.height)

    def onResize(sig, action):
        print(term.clear())
        weekView.resize(getFullBox())
        weekView.render()

    weekView = WeekView(getFullBox(), week_events)

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        # render
        # def render():
        #     print(term.clear())
        #     shapes.box(border)
        #     d.render()
        #     hourView.render()
            # print("lph: " , scale.lines_per_hour)
            # print("last time: " , scale.last_time_shown)

        # signal.signal(signal.SIGWINCH, lambda sig, action: render())
        signal.signal(signal.SIGWINCH, onResize)

        while True:
            weekView.render()
            key = term.inkey()
            if key == 'j':
                weekView.scroll_down()
            elif key == 'k':
                weekView.scroll_up()
            elif key == '-':
                scale.zoom_out()
            elif key == '+':
                scale.zoom_in()
            elif key == '>':
                d.box.width += 2
            elif key == '<':
                d.box.width -= 2
            elif key == 'q':
                exit()
