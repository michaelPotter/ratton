#!/usr/bin/env python3
#
# test.py
#
# Michael Potter
# 2020-07-15

from blessed import Terminal

import os.path
from pager import Pager
import linepager
from models import *
from util import *
import keysink
import shapes
import readline
import subprocess
import re


def get_app_keysink(pager):
    def sink(key):
        if key == 'q':
            exit()
        elif key == ':':
            global mode
            mode = "cmdline"
        elif key.code == term.KEY_ENTER:
            match = re.search("^d", pager.get_focused_line())
            if (match):
                d = pager.get_focused_line().split()[8]
                global current_dir
                current_dir = f"{current_dir}/{d}"
                show_dir(current_dir)
        else:
            return False
    return sink


def cmd_line_mode():
    with term.location(0, term.height-1):

        cmd = input(":")

        pager.draw()
        if cmd.strip() == "q":
            exit()


def show_dir(dirname):
    proc = subprocess.run(["ls", "-al", os.path.expanduser(dirname)], capture_output=True)
    text = proc.stdout.decode('utf-8')

    pager_box = Box(Point(0,0), width=term.width, height=term.height-2 )
    pager = linepager.LinePager(pager_box, text)

    sink = keysink.MultiKeysink()
    sink.add(keysink.get_pager_keysink(pager))
    sink.add(get_app_keysink(pager))

    with term.fullscreen():
        print(term.clear)
        global mode
        mode = "pager"
        pager.draw()
        pager.focus()
        while True:
            if mode == "pager":
                with term.cbreak():
                    key = term.inkey()
                    sink.apply(key)
            elif mode == "cmdline":
                cmd_line_mode()
                mode = "pager"



if __name__ == "__main__":
    current_dir = "~/mail"
    show_dir(current_dir)
