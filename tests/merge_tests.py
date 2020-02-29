#!/usr/bin/env python
# -*- coding: utf-8 -*-


merge_test_suite = {
"name": "Merge empty cells tests",
"scenarios": [
{
"name": "Short option test",
"args": ["-b", "basic", "-m"],
"input": '''\
1,,,5
,,6
4,5
1,22,,66
''' ,
"output": '''\
+---+----+----+
| 1 | 5  |    |
| 6 |    |    |
| 4 | 5  |    |
| 1 | 22 | 66 |
+---+----+----+
'''
},
{
"name": "Short option test",
"args": ["-b", "basic", "--merge-empty-cell"],
"input": '''\
,,,5
,,6
4,5
1,22,,66
''' ,
"output": '''\
+---+----+----+
| 5 |    |    |
| 6 |    |    |
| 4 | 5  |    |
| 1 | 22 | 66 |
+---+----+----+
'''
},
]}
