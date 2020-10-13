#!/usr/bin/env python3
#
# day.py
#
# Michael Potter
# 2020-10-07

from datetime import date, time, timedelta, datetime

from ratton.lib.util import *
from ratton.lib.models import *
import ratton.lib.shapes as shapes
import textwrap
import math

class HourScale(object):
    """
    A class to handle calculations about where to position a time on a scale.
    e.g. given a box of height 6, where the first line represents 9am, where do
    we put 10:30?
    """
    # FIXME start time is forced to be on a round hour and all calculations are
    # based on that.
    def __init__(self, height, lines_per_hour, start):
        self.height = height
        self.lines_per_hour = lines_per_hour
        self.start = start

    def get_position(self, time):
        """
        Returns the
        """
        # TODO handle hours that are too big? or just let clients deal w/it
        if time < self.start:
            return -1

        hour_diff = time.hour - self.start.hour
        minute_lines = math.floor((time.minute - self.start.minute) / self.minutes_per_line)
        # print("minutes_per_line", self.minutes_per_line)

        return hour_diff * self.lines_per_hour + minute_lines

    @property
    def last_time_shown(self):
        """
        Return the last time that can possibly be shown
        """
        hour = self.height // self.lines_per_hour + self.start.hour
        fraction = self.height / self.lines_per_hour + self.start.hour
        minute = math.floor((fraction - hour) * 60)
        return time(hour, minute)

    @property
    def minutes_per_line(self):
        return 60 / self.lines_per_hour

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        # forcing the start to be on an hour for simplicity
        # FIXME
        self._start = time(start.hour)

    def zoom_in(self):
        if self.lines_per_hour >= 6:
            self.lines_per_hour += 2
        elif self.lines_per_hour >= 2:
            self.lines_per_hour += 1

    def zoom_out(self):
        # FIXME if you're near/at the bottom it crashes
        if self.lines_per_hour > 6:
            self.lines_per_hour -= 2
        elif self.lines_per_hour > 2:
            self.lines_per_hour -= 1

    def scroll_up(self):
        if self.start.hour > 0:
            self.start = time(self.start.hour - 1)

    def scroll_down(self):
        # FIXME can't show events past 11:00
        if self.last_time_shown.hour < 23:
            self.start = time(self.start.hour + 1)


class HourScaleView(object):
    """
    A view that renders the hours along a vertical scale
    """
    def __init__(self, box, hourscale):
        self.box = box
        self.hourscale = hourscale

    def render(self):
        # print(self.hourscale.last_time_shown)
        start = self.hourscale.start

        # show half after if there's room
        lp = self.hourscale.lines_per_hour
        if lp < 4:
            minute_range = [0]
        elif lp == 4:
            minute_range = [0, 30]
        elif lp == 5:
            minute_range = [0, 24, 36]
        elif lp == 6:
            minute_range = [0, 20, 40]
        elif lp == 7:
            minute_range = [0, 20, 40]
            minute_range = range(0, 60, 12)
        elif lp == 8:
            minute_range = range(0, 60, 15)
        else:
            minute_range = [0, 30]

        for h in range(start.hour, self.hourscale.last_time_shown.hour + 1):
            for m in minute_range:
                b = term.bold if m == 0 else lambda x: x
                t = time(h, m)
                printat(self.box.x,
                        self.box.y + self.hourscale.get_position(t),
                        b(t.strftime("%I:%M")))



class DayView(object):
    """docstring for Day"""
    def __init__(self, box, events, hourscale):
        super(DayView, self).__init__()
        self.box = box
        self.events = events
        self.hourscale = hourscale


    def render(self):
        layout_events(self.events)
        for e in self.events:
            ev = EventView(e, self.box.offset(self._get_event_box(e)))
            ev.render()

    def _get_event_box(self, event):
        """
        Returns the box an event should take up within the DayView box
        The event should have the left and right props set layout_events
        """
        last_line = self.box.height - 1

        start = self.hourscale.get_position(event.start)
        if start < 0:
            start = 0
        elif start > last_line:
            return None

        endtime = datetime.combine(date.today(), event.end) - timedelta(minutes=1)
        end = self.hourscale.get_position(endtime.time())
        if end > last_line:
            end = last_line
        elif end < 0:
            return None

        left = math.floor(self.box.width * event.left)
        right = math.floor(self.box.width * event.right) - 1

        return Box(Point(left, start), Point(right, end))


def layout_events(events):
    """
    See https://stackoverflow.com/questions/11311410

    1. Think of an unlimited grid with just a left edge.
    2. Each event is one cell wide, and the height and vertical position is
       fixed based on starting and ending times.
    3. Try to place each event in a column as far left as possible, without
       it intersecting any earlier event in that column.
    4. Then, when each connected group of events is placed, their actual
       widths will be 1/n of the maximum number of columns used by the
       group.
    5. You could also expand the events at the far left and right to use up
       any remaining space.
    """

    def _layout_events(events):
        # 2d list. Each item represents a column, and should be a list of events.
        columns = []

        lastEnding = None
        for e in sorted(events, key=lambda e:e.start):

            # if (lastEnding and e.start >= lastEnding):
            #     pack_events(columns)
            #     lastEnding = None

            placed = False
            for col in columns:
                if col and not col[-1].intersects(e):
                    col.append(e)
                    placed = True
                    break

            # if e doesn't fit into any existing cols (or there are none),
            # add a new one
            if not placed:
                columns.append([e])

            if lastEnding is None or e.end > lastEnding:
                lastEnding = e.end

        if len(columns) > 0:
            pack_events(columns)

    def pack_events(columns):
        """
        Step 4. set the widths of each event
        """
        for i,col in enumerate(columns):
            for event in col:
                colspan = expand_events(event, i, columns)
                event.left = i / len(columns)
                event.right = (i + colspan) / len(columns)

    def expand_events(event, icolumn, columns):
        """
        Step 5. expand events where there is space
        """
        colspan = 1
        for c in columns[icolumn + 1:]:
            for e in c:
                if e.intersects(event):
                    return colspan
            colspan += 1
        return colspan

    _layout_events(events)




class EventCollisionData(object):
    """
    This is a wrapper around an event that contains data about collisions with
    other events. This is (should be) only used internally within the DayView
    to determine how to lay out events.
    """
    def __init__(self, event, collisions=None, c_index=0, c_slots=1):
        # event is the event we're wrapping
        self.event = event
        # collisions is a list of other events which we may be colliding with
        self.collisions = collisions
        if self.collisions == None:
            self.collisions = []
        # c_index is the collision index of this event.
        # c_slots is the number of slots that are available to this event.
        #
        # e.g. if c_index == 0 and c_slots == 2, this event should take up the left half.
        # if c_index == 1 and c_slots == 3, this event should take up the middle third.
        self.c_index = c_index
        self.c_slots = c_slots



class EventView(object):
    """
    View for an Event. Pass in an event object and a bounding box where the
    event should be rendered.
    """
    def __init__(self, event, box):
        self.event = event
        self.box = box

    def render(self):
        """
        Render the event.

        If the event display only takes up 1 line, just print a truncated
        description. If the event takes up two or more lines, the last line
        should (attempt to) show the time of the event, and the preceding lines
        should show the event text.
        """

        if self.box == None:
            return

        # draw the outline
        shapes.color_block(self.event.color, self.box)

        def print_text(text, line_num):
            attr = f"black_on_{self.event.color}"
            printat(self.box.x, self.box.y + line_num,
                    getattr(term, attr)(text))

        lines = textwrap.wrap(self.event.text)
        time = self._build_time_string()

        if self.box.height == 1:
            print_text(lines[0], 0)
        else:
            for i in range(self.box.height):
                if i < len(lines):
                    print_text(lines[i], i)
            print_text(time, self.box.height - 1)



    def _build_time_string(self):
        # TODO add am/pm?
        # TODO what if width == 10 and time is 11:30-12:30 (11)
        s = self.event.start
        e = self.event.end

        def format(t):
            if t.minute == 0:
                return t.strftime("%I").lstrip('0') # just hour
            else:
                return t.strftime("%I:%M").lstrip('0') # hour:minute
        start = format(s)
        end   = format(e)

        t = f"{start}-{end}"

        return t




class Event(object):
    def __init__(self, start, end, text, color):
        self.start = start
        self.end = end
        self.text = text
        self.color = color

    def intersects(self, other):
        return self.start < other.end and other.start < self.end



if __name__ == "__main__":
    h=26
    box = Box(Point(60,10), width=10, height=h)
    border = box.bound_outer()
    events = [
            Event(time(9, 30), time(9, 45), 'Standup', 'magenta'),
            Event(time(12, 00), time(13, 00), 'Lunch', 'green'),
            Event(time(13, 00), time(14, 00), 'Planning', 'blue'),
            Event(time(12, 30), time(13, 30), 'Collision', 'red'),
            ]

    scale_box = Box(Point(53, 10), width=5, height=h)
    scale = HourScale(box.height, 3, time(9))
    hourView = HourScaleView(scale_box, scale)

    d = DayView(box, events, scale)


    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        # render
        def render():
            print(term.clear())
            shapes.box(border)
            d.render()
            hourView.render()
            # print("lph: " , scale.lines_per_hour)
            # print("last time: " , scale.last_time_shown)


        while True:
            render()
            key = term.inkey()
            if key == 'j':
                scale.scroll_down()
            if key == 'k':
                scale.scroll_up()
            if key == '-':
                scale.zoom_out()
            if key == '+':
                scale.zoom_in()
            elif key == 'q':
                exit()
