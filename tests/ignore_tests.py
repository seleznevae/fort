#!/usr/bin/env python
# -*- coding: utf-8 -*-


ignore_test_suit = {
"name": "Ignore empty tests",
"scenarios": [
{
"name": "Short option test",
"args": ["-b", "basic", "-e"],
"input": '''\
1,3,5

4,5

1,22,33,66
''' ,
"output": '''\
+---+----+----+----+
| 1 | 3  | 5  |    |
| 4 | 5  |    |    |
| 1 | 22 | 33 | 66 |
+---+----+----+----+
'''
},
{
"name": "Long option test",
"args": ["-b", "basic", "--ignore-empty-lines"],
"input": '''\
1,3,5

4,5

1,22,33,66
''' ,
"output": '''\
+---+----+----+----+
| 1 | 3  | 5  |    |
| 4 | 5  |    |    |
| 1 | 22 | 33 | 66 |
+---+----+----+----+
'''
}
]}
