TextLand
========

Like wayland, for text apps, because using curses sucks

Example
=======

See demos in the top-level directory

Environment
===========

TEXTLAND_DISPLAY can be set to one of the following strings:

 * ``curses`` (default): to use the ncurses interface
 * ``print``: to use portable printer 80x25 "display"
 * ``test``: to use a off-screen display that replays injected test events and
   records all the screens that were "displayed"
