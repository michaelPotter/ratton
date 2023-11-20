#!/usr/bin/env python3
#
# mail.py
#
# Michael Potter
# 2021-01-26

from blessed import Terminal
from ratton.lib.util import *
from ratton.lib.models import *
import ratton.lib.shapes as shapes


messages = [
    ' 1 N + AMATH 301 on Piazza    [ ] Question about Lecture 12                                                                                Mon, Jan 25  07:53 PM',
    ' 2 N + UW Today               [ ] New developments in tissue engineering // Design students supporting Black-owned restaurants // more     Mon, Jan 25  05:01 AM',
    ' 3   + AMATH 301 on Piazza    [ ] [Instr Note] Announcement Video                                                                          Sun, Jan 24  08:14 PM',
    ' 4   + AMATH 301 A Wi 21: B   [ ] Announcement Video: AMATH 301 A Wi 21: Beginning Scientific Computing                                    Sun, Jan 24  08:13 PM',
    ' 5 N + Sona                   [ ] [Crucible] MYPLAN-2067: REGXP-2575 Added a cookie to capture ...                                         Fri, Jan 22  12:34 PM',
    ' 6   T UW-IT Service Center   [ ] [ UW REQ4325027 ] Notify dev CourseAddDrop Events                                                        Fri, Jan 22  08:57 AM',
    ' 7 N + UW Today               [ ] A stellar dance // Approaches to teaching during the pandemic // more                                    Fri, Jan 22  05:01 AM',
    ' 8   + Glenn Sudduth          [ ] ┌─>[Crucible] MYPLAN-2065: REGXP-2561 Added HttpClient for PATCH...                                      Thu, Jan 21  05:22 PM',
    ' 9   + Sona                   [ ] ┴─>[Crucible] MYPLAN-2065: REGXP-2561 Added HttpClient for PATCH...                                      Thu, Jan 21  03:19 PM',
    '10 N + Inside UW-IT News      [ ] Your excellent work showcased in Partnerships report // More Financial Aid Modernization // Challenge of Thu, Jan 21  05:00 PM',
    '11 N T UW-IT Service Center   [ ] [ UW REQ4325027 ] Notify dev CourseAddDrop Events                                                        Thu, Jan 21  04:37 PM',
]

def main():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        pager_border = Box(Point(2,0), width=82, height=26)
        shapes.box(pager_border, "fancy")

        # for i,m in enumerate(messages):
        #     printat(0,i,m)
        # current_time()
        # print_times()
        # print_days()
        # sample_events()

        # ticker = Ticker("Events w/ long text could scroll (11-11:30am)", Box(Point(mon.x,7), width=day_width-1, height=1))

        # # line numbers
        # for i in range(1,24):
        #     printat(0,i,i)

        while True:
            # ticker.render()
            # ticker.tick()
            key = term.inkey(timeout=0.3)
            if key == 'q':
                exit()

if __name__ == "__main__":
    main()
