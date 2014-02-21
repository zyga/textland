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

"""
Text Land
=========
"""

__version__ = (0, 1, 0, "final", 0)

__all__ = [
    'Cell',
    'BLACK',
    'BLUE',
    'CYAN',
    'GREEN',
    'MAGENTA',
    'RED',
    'WHITE',
    'YELLOW',
    'BRIGHT_BLACK',
    'BRIGHT_BLUE',
    'BRIGHT_CYAN',
    'BRIGHT_GREEN',
    'BRIGHT_MAGENTA',
    'BRIGHT_RED',
    'BRIGHT_WHITE',
    'BRIGHT_YELLOW',
    'DrawingContext',
    'EVENT_KEYBOARD',
    'EVENT_MOUSE',
    'EVENT_RESIZE',
    'NORMAL',
    'REVERSE',
    'UNDERLINE',
    'Event',
    'IApplication',
    'IDisplay',
    'KeyboardData',
    'MouseData',
    'Rect',
    'Size',
    'TestDisplay',
    'TextImage',
    'get_display',
    '__version__',
]

from .abc import IApplication
from .abc import IDisplay
from .attribute import NORMAL
from .attribute import REVERSE
from .attribute import UNDERLINE
from .bits import Cell
from .bits import Rect
from .bits import Size
from .colors import BLACK
from .colors import BLUE
from .colors import BRIGHT_BLACK
from .colors import BRIGHT_BLUE
from .colors import BRIGHT_CYAN
from .colors import BRIGHT_GREEN
from .colors import BRIGHT_MAGENTA
from .colors import BRIGHT_RED
from .colors import BRIGHT_WHITE
from .colors import BRIGHT_YELLOW
from .colors import CYAN
from .colors import GREEN
from .colors import MAGENTA
from .colors import RED
from .colors import WHITE
from .colors import YELLOW
from .display import TestDisplay
from .display import get_display
from .drawing import DrawingContext
from .events import EVENT_KEYBOARD
from .events import EVENT_MOUSE
from .events import EVENT_RESIZE
from .events import Event
from .events import KeyboardData
from .events import MouseData
from .image import TextImage
