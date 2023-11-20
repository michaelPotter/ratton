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

def get_test_data():
    sun = []
    mon = [
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            Event(time(11), time(11, 30), 'busy', 'red'),
            Event(time(13, 30), time(14), 'busy', 'red'),
            Event(time(15), time(15, 30), 'busy', 'red'),
            Event(time(16), time(17), 'appt', 'blue'),
            ]
    tue = [
            Event(time(7, 30), time(8), 'busy', 'red'),
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            ]
    wed = [
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            Event(time(10), time(11), 'busy', 'red'),
            Event(time(14, 30), time(15), 'busy', 'red'),
            Event(time(15), time(16), 'busy', 'red'),
            ]
    thu = [
            Event(time(7, 30), time(8), 'busy', 'red'),
            Event(time(8, 45), time(10, 15), 'busy', 'red'),
            Event(time(9), time(10), 'busy', 'red'),
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            Event(time(10, 30), time(11, 20), 'busy', 'red'),
            Event(time(14, 30), time(17, 30), 'busy', 'red'),
            Event(time(15), time(15, 30), 'busy', 'red'),
            ]
    fri = [
            Event(time(8, 30), time(9), 'busy', 'red'),
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            Event(time(10, 35), time(11, 25), 'busy', 'red'),
            Event(time(11, 40), time(12, 40), 'busy', 'red'),
            Event(time(13, 40), time(14, 30), 'busy', 'red'),
            Event(time(14, 45), time(15, 35), 'busy', 'red'),
            Event(time(14, 45), time(15, 35), 'busy', 'red'),
            Event(time(15, 50), time(17, 20), 'busy', 'red'),
            ]
    sat = []
    week_events = [
         Day("Sun 01", sun),
         Day("Mon 02", mon),
         Day("Tue 03", tue),
         Day("Wed 04", wed),
         Day("Thu 05", thu),
         Day("Fri 06", fri),
         Day("Sat 07", sat),
         ]

    return week_events


if __name__ == "__main__":
    h=26
    box = Box(Point(60,10), width=10, height=h)
    border = box.bound_outer()

    week_events = get_test_data()


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
        signal.signal(signal.SIGWINCH, onResize)

        while True:
            weekView.render()
            key = term.inkey()
            if key == 'j':
                weekView.scroll_down()
            elif key == 'k':
                weekView.scroll_up()
            elif key == '-':
                weekView.zoom_out()
            elif key == '+':
                weekView.zoom_in()
            # elif key == '>':
            #     d.box.width += 2
            # elif key == '<':
            #     d.box.width -= 2
            elif key == 'q':
                exit()
