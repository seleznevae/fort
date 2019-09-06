#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


##############  Input UTF-8 cases  ##################
input_utf8_test_suite = {
"name": "Input UTF-8 tests",
"scenarios": [
{
"name": "input from file",
"args": ["-b", "basic", "tmp_file"],
"beforeScript": "echo  'Мама|мыла\nРа|мумумумумум' > tmp_file",
"input": "",
"output": u'''\
+------+-------------+
| Мама | мыла        |
| Ра   | мумумумумум |
+------+-------------+
'''
}
]}
test_suites.append(input_utf8_test_suite)

##############  Long input strings cases  ##################
big_string_1 = 'a'*56784 + '1'
big_string_2 = 'a'*56783 + '2'
big_string_3 = 'a'*56783 + '3'
big_string_4 = 'a'*56784 + '4'
long_input_test_suite = {
"name": "Long input tests",
"scenarios": [
{
"name": "long input",
"args": [],
"input": '{}|{}\n{}|{}'.format(big_string_1,big_string_2,big_string_3,big_string_4) ,
"output": ' {}  {}  \n {}   {} \n'.format(big_string_1,big_string_2,big_string_3,big_string_4) 
}
]}
test_suites.append(long_input_test_suite)

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

###############  Merge empty cells test cases  ##################
merge_empty_cell_test_suite = {
"name": "Merge empty cells tests",
"scenarios": [
{
"name": "Short option test",
"args": ["-b", "basic", "-m"],
"input": '''\
1|||5
||6
4|5
1|22||66
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
|||5
||6
4|5
1|22||66
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
test_suites.append(merge_empty_cell_test_suite)

###############  Ignore empty lines test cases  ##################
ignore_empty_test_suite = {
"name": "Ignore empty tests",
"scenarios": [
{
"name": "Short option test",
"args": ["-b", "basic", "-e"],
"input": '''\
1|3|5

4|5

1|22|33|66
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
1|3|5

4|5

1|22|33|66
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
test_suites.append(ignore_empty_test_suite)

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
]}
test_suites.append(separator_test_suite)

###############  Row separator test cases  ##################

row_separator_test_suite = {
"name": "Row separator tests",
"scenarios": [
{
"name": "simple row separator test",
"args": ["-b", "basic", "-S", ";"],
"input": '''1|3;4|5;;5|6|7''' ,
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
"input": '''1|3;4|5:&5|6|7''' ,
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
test_suites.append(row_separator_test_suite)


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
test_suites.append(header_test_suite)

###############  Border styles test cases  ##################

border_styles_test_suite = {
"name": "Border styles tests",
"scenarios": [
{
"name": "basic border style",
"args": ["-b", "basic", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
| 5 | 6 |
+---+---+
'''
},
{
"name": "basic2 border style",
"args": ["-b", "basic2", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
+---+---+
| 1 | 2 |
+---+---+
| 3 | 4 |
+---+---+
| 5 | 6 |
+---+---+
'''
},
{
"name": "simple border style",
"args": ["-b", "simple", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
 1   2 
--- ---
 3   4 
 5   6 
'''
},
{
"name": "plain border style",
"args": ["-b", "plain", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
-------
 1   2 
-------
 3   4 
 5   6 
'''
},
{
"name": "dot border style",
"args": ["-b", "dot", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
.........
: 1 : 2 :
:...:...:
: 3 : 4 :
: 5 : 6 :
:...:...:
'''
},
{
"name": "empty border style",
"args": ["-b", "empty", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
 1  2 
 3  4 
 5  6 
'''
},
{
"name": "empty2 border style",
"args": ["-b", "empty2", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": '''\
         
  1   2  
  3   4  
  5   6  
         
'''
},
{
"name": "solid border style",
"args": ["-b", "solid", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
┌───┬───┐
│ 1 │ 2 │
├───┼───┤
│ 3 │ 4 │
│ 5 │ 6 │
└───┴───╯
'''
},
{
"name": "solid_round border style",
"args": ["-b", "solid_round", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
╭───┬───╮
│ 1 │ 2 │
├───┼───┤
│ 3 │ 4 │
│ 5 │ 6 │
╰───┴───╯
'''
},
{
"name": "nice border style",
"args": ["-b", "nice", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
╔═══╦═══╗
║ 1 ║ 2 ║
╠═══╬═══╣
║ 3 ║ 4 ║
║ 5 ║ 6 ║
╚═══╩═══╝
'''
},
{
"name": "double border style",
"args": ["-b", "double", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
╔═══╦═══╗
║ 1 ║ 2 ║
╠═══╬═══╣
║ 3 ║ 4 ║
║ 5 ║ 6 ║
╚═══╩═══╝
'''
},
{
"name": "double2 border style",
"args": ["-b", "double2", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
╔═══╤═══╗
║ 1 │ 2 ║
╠═══╪═══╣
║ 3 │ 4 ║
╟───┼───╢
║ 5 │ 6 ║
╚═══╧═══╝
'''
},
{
"name": "bold border style",
"args": ["-b", "bold", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
┏━━━┳━━━┓
┃ 1 ┃ 2 ┃
┣━━━╋━━━┫
┃ 3 ┃ 4 ┃
┃ 5 ┃ 6 ┃
┗━━━┻━━━┛
'''
},
{
"name": "bold2 border style",
"args": ["-b", "bold2", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
┏━━━┯━━━┓
┃ 1 │ 2 ┃
┣━━━┿━━━┫
┃ 3 │ 4 ┃
┠───┼───┨
┃ 5 │ 6 ┃
┗━━━┷━━━┛
'''
},
{
"name": "frame border style",
"args": ["-b", "frame", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": u'''\
▛▀▀▀▀▀▀▀▜
▌ 1 ┃ 2 ▐
▌━━━╋━━━▐
▌ 3 ┃ 4 ▐
▌ 5 ┃ 6 ▐
▙▄▄▄▄▄▄▄▟
'''
},
{
"name": "incorrect border style",
"args": ["-b", "abraCadabra", "--header=0"],
"input": '''\
1|2
3|4
5|6
''' ,
"output": "fort: error: Invalid border style\n",
"exitCode": 1
},
]}
test_suites.append(border_styles_test_suite)



for test_suite in test_suites:
    print "Running {}".format(test_suite["name"])
    for test_case in test_suite["scenarios"]:
        print "  Executing {}".format(test_case["name"])
        if "beforeScript" in test_case:
            os.system(test_case["beforeScript"])

        process = Popen(["../fort"] + test_case["args"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
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
        output = output_b.decode('utf-8')
        if output != test_case["output"]:
            print ' Test Failed'
            print '  Input'
            print test_case["input"]
            print '  Expected'
            print test_case["output"]
            print '  Recieved'
            print output
            sys.exit("Test failed!")
