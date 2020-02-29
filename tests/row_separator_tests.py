#!/usr/bin/env python
# -*- coding: utf-8 -*-


row_separator_test_suite = {
"name": "Row separator tests",
"scenarios": [
{
"name": "simple row separator test",
"args": ["-b", "basic", "-S", ";"],
"input": '''1,3;4,5;;5,6,7''' ,
"output": '''\
+---+---+---+
| 1 | 3 |   |
| 4 | 5 |   |
|   |   |   |
| 5 | 6 | 7 |
+---+---+---+
'''
},
{
"name": "Multiple row separators test",
"args": ["-b", "basic", "--row-separator=;:&"],
"input": '''1,3;4,5:&5,6,7''' ,
"output": '''\
+---+---+---+
| 1 | 3 |   |
| 4 | 5 |   |
|   |   |   |
| 5 | 6 | 7 |
+---+---+---+
'''
},
]}
