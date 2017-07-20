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
import collections, uno, re
from os.path import join as pathjoin

from unotools import Socket, connect
from unotools.component.writer import Writer
from unotools.unohelper import convert_path_to_url

PARAGRAPH_BREAK = uno.getConstantByName("com.sun.star.text.ControlCharacter.PARAGRAPH_BREAK")


def get_docstrings(modules, search_for=""):
    """Gathers docstrings from a list of modules
    For now, this function only supports variables and functions
    See get_comments_of_variables function to learn documenting variables in PINCE style

    Args:
        modules (list): A list of modules
        search_for (str): String that will be searched in variables and functions

    Returns:
        dict: A dict containing docstrings for documented variables and functions
        Format-->{variable1:docstring1, variable2:docstring2, ...}
    """
    element_dict = {}
    variable_comment_dict = get_comments_of_variables(modules)
    for item in modules:
        for key, value in item.__dict__.items():
            name_with_module = get_module_name(item) + "." + key
            if name_with_module in variable_comment_dict:
                element_dict[name_with_module] = variable_comment_dict[name_with_module]
            else:
                element_dict[name_with_module] = value.__doc__
    for item in list(element_dict):
        if item.split(".")[-1].find(search_for) == -1:
            del element_dict[item]
    return element_dict


def get_comments_of_variables(modules, search_for=""):
    """Gathers comments from a list of modules
    Python normally doesn't allow modifying __doc__ variable of the variables
    This function is designed to bring a solution to this problem
    The documentation must be PINCE style. It must start with this--> "#:doc:"
    See examples for more details

    Args:
        modules (list): A list of modules
        search_for (str): String that will be searched in variables

    Returns:
        dict: A dict containing docstrings for documented variables
        Format-->{variable1:docstring1, variable2:docstring2, ...}

    Example for single line comments:
        Code--▼
            #:doc:
            #Documentation for the variable
            some_variable = blablabla
        Returns--▼
            {"some_variable":"Documentation for the variable"}

    Example for multi line comments:
        Code--▼
            #:doc:
            '''Some Header
            Documentation for the variable
            Some Ending Word'''
            some_variable = blablabla
        Returns--▼
            {"some_variable":"Some Header\nDocumentation for the variable\nSome Ending Word"}
    """
    comment_dict = {}
    source_files = []
    for module in modules:
        source_files.append(module.__file__)
    for index, file_path in enumerate(source_files):
        source_file = open(file_path, "r")
        lines = source_file.readlines()
        for row, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line.startswith("#:doc:"):
                docstring_list = []
                while True:
                    row += 1
                    current_line = lines[row].strip()
                    if current_line.startswith("#"):
                        docstring_list.append(current_line.replace("#", "", 1))
                    elif current_line.startswith("'''"):
                        current_line = current_line.replace("'''", "", 1)
                        if current_line.endswith("'''"):
                            current_line = current_line.replace("'''", "")
                            docstring_list.append(current_line)
                            continue
                        docstring_list.append(current_line)
                        while True:
                            row += 1
                            current_line = lines[row].strip()
                            if current_line.endswith("'''"):
                                current_line = current_line.replace("'''", "")
                                docstring_list.append(current_line)
                                break
                            docstring_list.append(current_line)
                    else:
                        while True:
                            stripped_current_line = re.search(r"(\w+)\s*=", current_line)
                            if stripped_current_line:
                                variable = stripped_current_line.group(1)
                                break
                            row += 1
                            current_line = lines[row].strip()
                        break
                if variable.find(search_for) == -1:
                    continue
                comment_dict[get_module_name(modules[index]) + "." + variable] = "\n".join(docstring_list)
    return comment_dict


def get_module_name(module):
    """Gets the name of the given module without the package name

    Args:
        module (module): A module

    Returns:
        str: Name of the module
    """
    return module.__name__.replace(module.__package__ + ".", "", 1)


def get_tags(modules, tag_to_string, search_for=""):
    """Gathers tags from a python source file
    The documentation must be PINCE style. It must start like this--> "#:tag:tag_name"
    For now, tagging system only supports variables and functions
    See examples for more details

    Args:
        modules (list): A list of modules
        tag_to_string (dict): A dictionary that holds tag descriptions in this format-->{tag:tag_description}
        Check test.tag_to_string for an example
        search_for (str): String that will be searched in tags

    Returns:
        dict: A dict containing tag keys for tagged variables
        Format-->{tag1_desc:variable_list1, tag2_desc:variable_list2, ...}

    Examples:
        Code--▼
            #:tag:tag_name
            #Documentation for the variable
            some_variable = blablabla

            or

            #:tag:tag_name
            def func_name(...)
        Returns--▼
            {tag_to_string["tag_name"]:list of some_variables or func_names that have the tag tag_name}
    """
    tag_dict = {}
    source_files = []
    for module in modules:
        source_files.append(module.__file__)
    for index, file_path in enumerate(source_files):
        source_file = open(file_path, "r")
        lines = source_file.readlines()
        for row, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line.startswith("#:tag:"):
                tag = stripped_line.replace("#:tag:", "", 1)
                while True:
                    row += 1
                    current_line = lines[row].strip()
                    stripped_current_line = re.search(r"def\s+(\w+)|(\w+)\s*=", current_line)
                    if stripped_current_line:
                        for item in stripped_current_line.groups():
                            if item:
                                if item.find(search_for) == -1:
                                    break
                                item = get_module_name(modules[index]) + "." + item
                                try:
                                    tag_dict[tag].append(item)
                                except KeyError:
                                    tag_dict[tag] = [item]
                                break
                            else:
                                continue
                        break
    ordered_tag_dict = collections.OrderedDict()
    for tag, desc in tag_to_string.items():
        if tag in tag_dict:
            ordered_tag_dict[desc] = tag_dict[tag]
        else:
            continue
    return ordered_tag_dict


def insert_paragraph(writer, cursor, text, style):
    """Inserts a paragraph to given writer at given cursor

    Args:
        writer (unotools.component.writer.Writer): The writer object
        cursor (unotools.component.writer.Writer.text.createTextCursor): The cursor object
        text (str): Inserted text
        style (str): Style of the cursor
    """
    cursor.ParaStyleName = style
    writer.text.insertString(cursor, text, 0)
    writer.text.insertControlCharacter(cursor, PARAGRAPH_BREAK, 0)


def create_tag_documents(module_list, tag_to_string, output_file_name,
                         search_for="", output_dir=".", host="localhost", port="8100", option=None):
    """Creates documents from tags in given modules. Check get_tags function to learn tagging

    Args:
        module_list (list): A list of modules
        tag_to_string (dict): A dictionary that holds tag descriptions in this format-->{tag:tag_description}
        Check test.tag_to_string for an example
        output_file_name (str): Shared name for the output files
        search_for (str): String that will be searched in tagged variables and functions
        output_dir (str): Output directory of the documents, defaults to the current directory
        host (str): host for the connect function
        port (str): port for the connect function
        option (str): options for the connect function, for instance-->"tcpNoDelay=1"
    """
    context = connect(Socket(host, port), option=option)
    writer = Writer(context)
    cursor = writer.text.createTextCursor()
    insert_paragraph(writer, cursor, "Tags", "Title")
    tag_dict = get_tags(module_list, tag_to_string, search_for)
    for tag in tag_dict:
        insert_paragraph(writer, cursor, tag, "Heading 3")
        for item in tag_dict[tag]:
            insert_paragraph(writer, cursor, "\t" + item, "Standard")
    insert_paragraph(writer, cursor, "Documentation", "Title")
    docstring_dict = get_docstrings(module_list, search_for)
    for tag in tag_dict:
        for item in tag_dict[tag]:
            docstring = docstring_dict[item]
            docstring = "\n".join(["\t" + item for item in docstring.splitlines()])
            insert_paragraph(writer, cursor, item, "Heading 5")
            insert_paragraph(writer, cursor, docstring, "Standard")
    base_path = convert_path_to_url(pathjoin(output_dir, output_file_name))
    writer.store_to_url(base_path + '.odt', 'FilterName', 'writer8')
    writer.store_to_url(base_path + '.doc', 'FilterName', 'MS Word 97')
    writer.store_to_url(base_path + '.pdf', 'FilterName', 'writer_pdf_Export')
    writer.store_to_url(base_path + '.html', 'FilterName', 'HTML (StarWriter)')
    writer.close(True)
