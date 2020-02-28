#!/usr/bin/env python
# -*- coding: utf-8 -*-


input_test_suite = {
"name": "Input tests",
"scenarios": [
{
"name": "invalid input file",
"args": ["dummy_name"],
"input": "",
"output": "fort: error: No such file or directory\n",
"exitCode": 1
},
{
"name": "input from file",
"args": ["-b", "basic", "tmp_file"],
"beforeScript": "echo  '1,3\n4,5' > tmp_file",
"input": "",
"output": '''\
+---+---+
| 1 | 3 |
| 4 | 5 |
+---+---+
''',
"afterScript": "rm tmp_file"
},
{
"name": "input from stdin",
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
"name": "input from stdin after dash",
"args": ["-b", "basic", "-"],
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
]}

