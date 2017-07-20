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
import sys


#:tag:misc
def get_current_script_directory():
    """Get current working directory

    Returns:
        str: A string pointing to the current working directory
    """
    return sys.path[0]


#:tag:util
def aob_to_str(list_of_bytes, encoding="ascii"):
    """Converts given array of hex strings to str

    Args:
        list_of_bytes (list): Must be returned from GDB_Engine.hex_dump()
        encoding (str): See here-->https://docs.python.org/3/library/codecs.html

    Returns:
        str: str equivalent of array
    """

    # 3f is ascii hex representation of char "?"
    return bytes.fromhex("".join(list_of_bytes).replace("??", "3f")).decode(encoding, "surrogateescape")


#:tag:util
def split_symbol(symbol_string):
    """Splits symbol part of type_defs.tuple_function_info into smaller fractions
    Fraction count depends on the the symbol_string. See Examples section for demonstration

    Args:
        symbol_string (str): symbol part of type_defs.tuple_function_info

    Returns:
        list: A list containing parts of the splitted symbol

    Examples:
        symbol_string-->"func(param)@plt"
        returned_list-->["func","func(param)","func(param)@plt"]

        symbol_string-->"malloc@plt"
        returned_list-->["malloc", "malloc@plt"]

        symbol_string-->"printf"
        returned_list-->["printf"]
    """
    returned_list = []
    if "(" in symbol_string:
        returned_list.append(symbol_string.split("(", maxsplit=1)[0])
    if "@" in symbol_string:
        returned_list.append(symbol_string.split("@", maxsplit=1)[0])
    returned_list.append(symbol_string)
    return returned_list
