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
import collections, unotagger
from test_libs import test_module1, test_module2, test_module3

# Check test_libs for an example of usage
# Format: {tag:tag_description}
tag_to_string = collections.OrderedDict([
    ("var", "Variables"),
    ("util", "Utilities"),
    ("misc", "Miscellaneous"),
])

unotagger.create_tag_documents([test_module1, test_module2, test_module3], tag_to_string, "tag_example")
unotagger.create_tag_documents([test_module1, test_module2, test_module3], tag_to_string, "tag_search_example", "bar")
