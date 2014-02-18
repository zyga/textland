# This file is part of textland.
#
# Copyright 2014 Canonical Ltd.
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
#
# Textland is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3,
# as published by the Free Software Foundation.
#
# Textland is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Textland.  If not, see <http://www.gnu.org/licenses/>.

from abc import abstractmethod
from collections import deque
from copy import deepcopy
from os import getenv

from . import keys
from .abc import IApplication
from .abc import IDisplay
from .bits import Size
from .events import Event, KeyboardData
from .events import EVENT_KEYBOARD, EVENT_RESIZE
from .image import TextImage


class AbstractDisplay(IDisplay):
    """
    Abstract display class.
    """

    def run(self, app: IApplication) -> None:
        """
        Run forever, feeding events to the controller
        the controller can raise StopIteration to "quit"
        """
        # Tell the app abount the initial size
        size = self.get_display_size()
        try:
            image = app.consume_event(Event(EVENT_RESIZE, size))
            self.display_image(image)
        except StopIteration:
            return
        # Then keep on running until the app raises StopIteration
        while True:
            try:
                # XXX: TestDisplay.wait_for_event() can raise StopIteration
                # but this is a hack that is not really applicable for curses
                event = self.wait_for_event()
                image = app.consume_event(event)
            except StopIteration:
                break
            else:
                self.display_image(image)

    @abstractmethod
    def display_image(self, image: TextImage) -> None:
        """
        Display the contents of the image on the screen
        """

    @abstractmethod
    def get_display_size(self) -> Size:
        """
        Get the current size of the display
        """

    @abstractmethod
    def wait_for_event(self) -> Event:
        """
        Get the next event, waiting for it to occur
        """


class PrintDisplay(AbstractDisplay):
    """
    A display that uses regular print() and input()
    """

    def __init__(self, size=Size(80, 25)):
        self.screen = TextImage(size)

    def display_image(self, image: TextImage) -> None:
        text_buffer = image.text_buffer
        width = self.screen.size.width
        height = self.screen.size.height
        print("/{}\\".format('=' * width))
        for y in range(height):
            line = text_buffer[y * width: (y + 1) * width].tounicode()
            print("|{}|".format(line))
        print("\\{}/".format('=' * width))

    def get_display_size(self) -> Size:
        return self.screen.size

    _commands = {
        'up': Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_UP)),
        'down': Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_DOWN)),
        'left': Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_LEFT)),
        'right': Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_RIGHT)),
        '': Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_ENTER)),
    }

    def wait_for_event(self) -> Event:
        while True:
            text = input("TextLand> ")
            try:
                return self._commands[text]
            except KeyError:
                if len(text) == 1:
                    return Event(EVENT_KEYBOARD, KeyboardData(text[0]))
                else:
                    print("Type command name or exactly one letter")


class CursesDisplay(AbstractDisplay):
    """
    A display using python curses module
    """

    def __init__(self):
        import curses
        self._curses = curses
        self._screen = None

    def run(self, app: IApplication) -> None:
        self._init_curses()
        try:
            return super().run(app)
        finally:
            self._fini_curses()

    def _init_curses(self):
        self._screen = self._curses.initscr()
        if self._curses.has_colors():
            self._curses.start_color()
            self._curses.use_default_colors()
        self._curses.noecho()
        self._curses.cbreak()
        self._screen.keypad(1)

    def _fini_curses(self):
        if self._screen is not None:
            self._screen.keypad(0)
        self._curses.echo()
        self._curses.nocbreak()
        self._curses.endwin()

    def display_image(self, image: TextImage) -> None:
        text_buffer = image.text_buffer
        width = image.size.width
        height = image.size.height
        for y in range(height - 1):
            line = text_buffer[y * width: (y + 1) * width].tounicode()
            self._screen.addstr(y, 0, line)
        y += 1
        line = text_buffer[y * width: (y + 1) * width].tounicode()
        self._screen.addstr(y, 0, line[:-1])
        self._screen.refresh()

    def get_display_size(self) -> Size:
        y, x = self._screen.getmaxyx()
        return Size(x, y)

    def wait_for_event(self) -> Event:
        key_code = self._screen.getch()
        if key_code == self._curses.KEY_RESIZE:
            return Event(EVENT_RESIZE, self.get_display_size())
        elif key_code == self._curses.KEY_UP:
            return Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_UP))
        elif key_code == self._curses.KEY_DOWN:
            return Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_DOWN))
        elif key_code == self._curses.KEY_LEFT:
            return Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_LEFT))
        elif key_code == self._curses.KEY_RIGHT:
            return Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_RIGHT))
        elif key_code == ord(' '):
            return Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_SPACE))
        elif key_code == ord('\n'):
            return Event(EVENT_KEYBOARD, KeyboardData(keys.KEY_ENTER))
        else:
            return Event(EVENT_KEYBOARD, KeyboardData(chr(key_code)))


class TestDisplay(AbstractDisplay):
    """
    A display that records all images and replays pre-recorded events
    """

    def __init__(self, size=Size(80, 25)):
        self.screen_log = []
        self.size = size
        self.events = deque()

    def display_image(self, image: TextImage) -> None:
        self.screen_log.append(deepcopy(image))

    def get_display_size(self) -> Size:
        return self.size

    def wait_for_event(self) -> Event:
        try:
            return self.events.popleft()
        except IndexError:
            raise StopIteration

    def inject_event(self, event: Event) -> None:
        """
        Inject an event.

        Events are served in FIFO mode.
        """
        self.events.append(event)


def get_display(display=None) -> IDisplay:
    """
    Get a ITextDisplay according to TEXTLAND_DISPLAY environment variable
    """
    if display is None:
        display = getenv("TEXTLAND_DISPLAY", "curses")
    if display == "curses":
        try:
            return CursesDisplay()
        except ImportError:
            # Sized like that to fit 80x25 without any overflow
            return PrintDisplay(Size(77, 22))
    elif display == "print":
        return PrintDisplay()
    elif display == "test":
        return TestDisplay()
    else:
        raise ValueError("Unsupported TEXTLAND_DISPLAY type")
