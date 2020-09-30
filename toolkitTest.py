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

import os.path
import subprocess

proc = subprocess.run(["ls", "-al", os.path.expanduser("~")], capture_output=True)
text = proc.stdout.decode('utf-8')

buffer = Buffer(document=Document(text), read_only=True)
buffer.cursor_position = 0 # start at top of document
bufferControl = BufferControl(buffer)
body = Window(bufferControl, cursorline=True)

kb = KeyBindings()

@kb.add("q")
def _(event):
    " Quit application. "
    event.app.exit()

@kb.add("h")
def _(event):
    buffer.cursor_left()
@kb.add("l")
def _(event):
    buffer.cursor_right()
@kb.add("j")
def _(event):
    buffer.cursor_down()
    # bufferControl.move_cursor_down()
@kb.add("k")
def _(event):
    bufferControl.move_cursor_up()
@kb.add("g", "g")
def _(event):
    buffer.cursor_position = 0
@kb.add("$")
def _(event):
    buffer.cursor_right(buffer.document.get_end_of_line_position())
@kb.add("G")
def _(event):
    # buffer.cursor_position = buffer.document.line_count
    buffer.cursor_position = len(buffer.text)

application = Application(layout=Layout(body), key_bindings=kb, full_screen=True)

def run():
    application.run()


if __name__ == "__main__":
    run()
