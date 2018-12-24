#!/usr/bin/env python

import subprocess
from subprocess import Popen, PIPE, STDOUT
from subprocess import call
import sys
import os


test_suites = []

##############  Input test cases  ##################
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
"beforeScript": "echo  '1|3\n4|5' > tmp_file",
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
"name": "input from stdin after dash",
"args": ["-b", "basic", "-"],
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
]}
test_suites.append(input_test_suite)




###############  Simple test cases  ##################

simple_test_suite = {
"name": "Simple tests",
"scenarios": [
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
}
]}
test_suites.append(simple_test_suite)


###############  Field separator test cases  ##################

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
]}
test_suites.append(separator_test_suite)


###############  Header test cases  ##################

header_test_suite = {
"name": "Header tests",
"scenarios": [
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
]}
test_suites.append(separator_test_suite)



for test_suite in test_suites:
    print "Running {}".format(test_suite["name"])
    for test_case in test_suite["scenarios"]:
        print "  Executing {}".format(test_case["name"])
        if "beforeScript" in test_case:
            os.system(test_case["beforeScript"])

        process = Popen(["./fort"] + test_case["args"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        (output_b, err) = process.communicate(input=test_case["input"])

        if "exitCode" in test_case:
            expCode = test_case["exitCode"]
        else:
            expCode = 0
        if expCode != process.returncode:
            print "Invalid return code: expected {}, recieved {}".format(expCode, process.returncode)

        if "afterScript" in test_case:
            os.system(test_case["afterScript"])

        if err:
            print "Error encountered: {}".format(err)
        output = output_b.decode('ascii')
        if output != test_case["output"]:
            print ' Test Failed'
            print '  Input'
            print test_case["input"]
            print '  Expected'
            print test_case["output"]
            print '  Recieved'
            print output
            sys.exit("Test failed!")
