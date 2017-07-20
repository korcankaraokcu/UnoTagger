# -*- coding: utf-8 -*-
"""
Copyright (C) 2017 Korcan Karaokçu <korcankaraokcu@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""


#:tag:misc
def center_scroll_bar(QScrollBar):
    """Center the given scrollbar

    Args:
        QScrollBar (QScrollbar): The scrollbar that'll be centered
    """
    maximum = QScrollBar.maximum()
    minimum = QScrollBar.minimum()
    QScrollBar.setValue((maximum + minimum) / 2)


#:tag:misc
def center_to_parent(window):
    """Center the given window to it's parent

    Args:
        window (QMainWindow, QWidget etc.): The window that'll be centered to it's parent
    """
    window.move(window.parent().frameGeometry().center() - window.frameGeometry().center())
