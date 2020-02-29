#!/usr/bin/env python
# -*- coding: utf-8 -*-


styles_test_suite = {
"name": "Border styles tests",
"scenarios": [
{
"name": "basic border style",
"args": ["-b", "basic", "--header=0"],
"input": '''\
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
''' ,
"output": u'''\
┌───┬───┐
│ 1 │ 2 │
├───┼───┤
│ 3 │ 4 │
│ 5 │ 6 │
└───┴───┘
'''
},
{
"name": "solid_round border style",
"args": ["-b", "solid_round", "--header=0"],
"input": '''\
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
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
1,2
3,4
5,6
''' ,
"output": "fort: error: Invalid border style\n",
"exitCode": 1
},
]}
