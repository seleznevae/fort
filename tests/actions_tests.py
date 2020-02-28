#!/usr/bin/env python
# -*- coding: utf-8 -*-


action_test_suite = {
"name": "Action tests",
"scenarios": [
{
"name": "Action for one line",
"args": ["-b", "basic", "--action=1fg-red"],
"input": '''\
0,1
2,3
4,5
''' ,
"output": u'''\
+---+---+
| 0 | 1 |
| \x1b[31m2\x1b[0m | \x1b[31m3\x1b[0m |
| 4 | 5 |
+---+---+
'''
},
{
"name": "Action for range of lines",
"args": ["-b", "basic", "--action=1,2fg-red"],
"input": '''\
0,1
2,3
4,5
6,7
''' ,
"output": u'''\
+---+---+
| 0 | 1 |
| \x1b[31m2\x1b[0m | \x1b[31m3\x1b[0m |
| \x1b[31m4\x1b[0m | \x1b[31m5\x1b[0m |
| 6 | 7 |
+---+---+
'''
},
{
"name": "Action by regex",
"args": ["-b", "basic", "--action=/.*33.*/fg-red"],
"input": '''\
0,1
2,1335
4,5
''' ,
"output": u'''\
+---+------+
| 0 | 1    |
| 2 | \x1b[31m1335\x1b[0m |
| 4 | 5    |
+---+------+
'''
},
{
"name": "Action by lines and regex",
"args": ["-b", "basic", "--action=1/.*33.*/fg-red"],
"input": '''\
0,1335
2,1335
4,5
''' ,
"output": u'''\
+---+------+
| 0 | 1335 |
| 2 | \x1b[31m1335\x1b[0m |
| 4 | 5    |
+---+------+
'''
}
]}
