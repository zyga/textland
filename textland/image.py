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

from array import array

from .bits import Cell, Size


class TextImage:
    """
    A rectangular, mutable text image.
    The image supports NORMAL, REVERSE and UNDERLINE as per-cell attributes.
    """

    def __init__(self, size: Size):
        self.size = size
        self.width = self.size.width
        self.text_buffer = array('u')
        self.text_buffer.extend(' ' * size.width * size.height)
        self.format_buffer = array('H')  # Unsigned short
        self.format_buffer.extend([0] * size.width * size.height)

    def put(self, x: int, y: int, c: str, attribute: int) -> None:
        # TODO: Add color support
        assert 0 <= x < self.size.width
        assert 0 <= y < self.size.height
        self.text_buffer[x + y * self.width] = c
        self.format_buffer[x + y * self.width] = attribute

    def get(self, x: int, y: int) -> Cell:
        # TODO: Add color support
        char = self.text_buffer[x + y * self.size.width]
        attribute = self.format_buffer[x + y * self.size.width]
        return Cell(char, attribute)

    def print_frame(self) -> None:
        text_buffer = self.text_buffer
        width = self.size.width
        height = self.size.height
        print("/{}\\".format('=' * width))
        for y in range(height):
            line = text_buffer[y * width: (y + 1) * width].tounicode()
            print("|{}|".format(line))
        print("\\{}/".format('=' * width))
