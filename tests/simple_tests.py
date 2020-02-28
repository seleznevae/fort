#!/usr/bin/env python
# -*- coding: utf-8 -*-


simple_test_suite = {
"name": "Simple tests",
"scenarios": [
{
"name": "simple test",
"args": ["-b", "basic"],
"input": '''\
1,3
4,5
''' ,
"output": '''\
+---+---+
| 1 | 3 |
| 4 | 5 |
+---+---+
'''
},
{
"name": "simple test 2",
"args": ["-b", "basic"],
"input": '''\
1,3,5

4,5
1,22,33,66
''' ,
"output": '''\
+---+----+----+----+
| 1 | 3  | 5  |    |
|   |    |    |    |
| 4 | 5  |    |    |
| 1 | 22 | 33 | 66 |
+---+----+----+----+
'''
}
]}