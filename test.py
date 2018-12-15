#!/usr/bin/env python

import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys

test_cases = [
{
"name": "simple test",
"args": ["-b", "basic"],
"input": '''\
1|3
4|5
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
1|3|5

4|5
1|22|33|66
''' ,
"output": '''\
+---+----+----+----+
| 1 | 3  | 5  |    |
|   |    |    |    |
| 4 | 5  |    |    |
| 1 | 22 | 33 | 66 |
+---+----+----+----+
'''
},
{
"name": "simple separator test",
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
"name": "simple header",
"args": ["-b", "basic", "--header=0,3"],
"input": '''\
1|2
3|4
5|6
7|8
9|0
1|2
3|4
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
]

for test_case in test_cases:
    print "Executing {}".format(test_case["name"])
    process = Popen(["./fort"] + test_case["args"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    (output_b, err) = process.communicate(input=test_case["input"])
    output = output_b.decode('ascii')
    if output != test_case["output"]:
        print ' Test Failed'
        print 'Input'
        print test_case["input"]
        print 'Expected'
        print test_case["output"]
        print 'Recieved'
        print output
        sys.exit("Test failed!")