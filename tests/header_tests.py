#!/usr/bin/env python
# -*- coding: utf-8 -*-


header_test_suite = {
"name": "Header tests",
"scenarios": [
{
"name": "simple header",
"args": ["-b", "basic", "--header=0,3"],
"input": '''\
1,2
3,4
5,6
7,8
9,0
1,2
3,4
''' ,
"output": '''\
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
+---+---+
| 7 | 8 |
+---+---+
| 9 | 0 |
| 1 | 2 |
| 3 | 4 |
+---+---+
'''
},
]}
