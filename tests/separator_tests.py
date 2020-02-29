#!/usr/bin/env python
# -*- coding: utf-8 -*-


separator_test_suite = {
"name": "Separator tests",
"scenarios": [
{
"name": "simple field separator test",
"args": ["-b", "basic", "-s", "%"],
"input": '''\
1%3
4%5
''' ,
"output": '''\
+---+---+
| 1 | 3 |
| 4 | 5 |
+---+---+
'''
},
{
"name": "Consecutive field separator test",
"args": ["-b", "basic", "-s", "|"],
"input": '''\
1|3
4||5
''' ,
"output": '''\
+---+---+---+
| 1 | 3 |   |
| 4 |   | 5 |
+---+---+---+
'''
},
{
"name": "Multiple field separators test",
"args": ["-b", "basic", "--col-separator=%^*"],
"input": '''\
1%3
4^5
7*8
''' ,
"output": '''\
+---+---+
| 1 | 3 |
| 4 | 5 |
| 7 | 8 |
+---+---+
'''
},
{
"name": "Spaces and tabs separators test",
"args": ["-b", "basic", "--col-separator= 	"],
"input": '''\
1	2 3
1 456	78	99
''' ,
"output": '''\
+---+-----+----+----+
| 1 | 2   | 3  |    |
| 1 | 456 | 78 | 99 |
+---+-----+----+----+
'''
},
]}

