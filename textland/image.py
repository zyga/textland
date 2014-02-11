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

from .bits import Size


class TextImage:
    """
    A rectangular, mutable text image.

    This image does not support any display attributes such as foreground color
    background color, underline, bold, etc.
    """

    def __init__(self, size: Size):
        self.size = size
        self.width = self.size.width
        self.text_buffer = array('u')
        self.text_buffer.extend(' ' * size.width * size.height)

    def put(self, x: int, y: int, c: str) -> None:
        assert 0 <= x < self.size.width
        assert 0 <= y < self.size.height
        self.text_buffer[x + y * self.width] = c

    def get(self, x: int, y: int) -> str:
        return self.text_buffer[x + y * self.width]

    def print_frame(self) -> None:
        text_buffer = self.text_buffer
        width = self.size.width
        height = self.size.height
        print("/{}\\".format('=' * width))
        for y in range(height):
            line = text_buffer[y * width: (y + 1) * width].tounicode()
            print("|{}|".format(line))
        print("\\{}/".format('=' * width))
