#!/usr/bin/env python3
#
# toolkitTest.py
#
# Michael Potter
# 2020-09-29

from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.document import Document
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.layout import Layout

import re
import os.path
import subprocess

def ls(path):
    proc = subprocess.run(["ls", "-al", os.path.expanduser(path)], capture_output=True)
    return proc.stdout.decode('utf-8')

kb = KeyBindings()
def add_bindings(buffer):
    @kb.add("h")
    def _(event):
        buffer.cursor_left()
    @kb.add("l")
    def _(event):
        buffer.cursor_right()
    @kb.add("j")
    def _(event):
        buffer.cursor_down()
    @kb.add("k")
    def _(event):
        buffer.cursor_up()
    @kb.add("g", "g")
    def _(event):
        buffer.cursor_position = 0
    @kb.add("$")
    def _(event):
        buffer.cursor_right(buffer.document.get_end_of_line_position())
    @kb.add("G")
    def _(event):
        buffer.cursor_position = len(buffer.text)
    @kb.add("enter")
    def _(event):
        match = re.search("^d", buffer.document.current_line)
        if (match):
            print(buffer.document.current_line)


def dirWindow(path):
    text = ls(path)
    buffer = Buffer(document=Document(text), read_only=True)
    buffer.cursor_position = 0 # start at top of document
    bufferControl = BufferControl(buffer)
    win = Window(bufferControl, cursorline=True)
    add_bindings(buffer)
    return win


win = dirWindow("~")


@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()


application = Application(
        layout=Layout(win),
        key_bindings=kb,
        full_screen=True,
        enable_page_navigation_bindings=True
        )

def run():
    application.run()


if __name__ == "__main__":
    run()
