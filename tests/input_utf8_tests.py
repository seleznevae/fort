#!/usr/bin/env python
# -*- coding: utf-8 -*-


##############  Input UTF-8 cases  ##################
# See http://clagnut.com/blog/2380/ for list of pangrams
# Note: doesn't work goog for all languages (e.g. for Thai)
input_utf8_test_suite = {
"name": "Input UTF-8 tests",
"scenarios": [
{
"name": "String in chinese",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
視野無限廣|窗外有藍天
微風迎客，軟語伴茶|中国智造
''',
"output": u'''\
+--------------------+------------+
| 視野無限廣         | 窗外有藍天 |
| 微風迎客，軟語伴茶 | 中国智造   |
+--------------------+------------+
'''
},
{
"name": "String in french",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
Voyez le brick|géant que
j’examine près du|wharf
''',
"output": u'''\
+-------------------+-----------+
| Voyez le brick    | géant que |
| j’examine près du | wharf     |
+-------------------+-----------+
'''
},
{
"name": "String in german",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
Victor jagt zwölf Boxkämpfer quer über den großen|Falsches Üben von Xylophonmusik quält jeden größeren Zwerg
Franz jagt im komplett verwahrlosten Taxi quer durch Bayern
''',
"output": u'''\
+-------------------------------------------------------------+------------------------------------------------------------+
| Victor jagt zwölf Boxkämpfer quer über den großen           | Falsches Üben von Xylophonmusik quält jeden größeren Zwerg |
| Franz jagt im komplett verwahrlosten Taxi quer durch Bayern |                                                            |
+-------------------------------------------------------------+------------------------------------------------------------+
'''
},
{
"name": "String in greek",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
Ταχίστη αλώπηξ βαφής ψημένη γη|δρασκελίζει υπέρ νωθρού κυνός Takhístè alôpèx vaphês psèménè gè
Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία|Xeskepazó tin psychofthóra vdelygmía
''',
"output": u'''\
+-----------------------------------+-----------------------------------------------------------------+
| Ταχίστη αλώπηξ βαφής ψημένη γη    | δρασκελίζει υπέρ νωθρού κυνός Takhístè alôpèx vaphês psèménè gè |
| Ξεσκεπάζω τὴν ψυχοφθόρα βδελυγμία | Xeskepazó tin psychofthóra vdelygmía                            |
+-----------------------------------+-----------------------------------------------------------------+
'''
},
{
"name": "String in japanese",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
いろはにほへと ちりぬるを わかよ|たれそ つねならむ うゐのおくやま けふこ
色は匂へど 散りぬるを 我が世誰ぞ 常ならむ 有|為の奥山 今日越えて 浅き夢見じ 酔ひもせず
''',
"output": u'''\
+----------------------------------------------+-------------------------------------------+
| いろはにほへと ちりぬるを わかよ             | たれそ つねならむ うゐのおくやま けふこ   |
| 色は匂へど 散りぬるを 我が世誰ぞ 常ならむ 有 | 為の奥山 今日越えて 浅き夢見じ 酔ひもせず |
+----------------------------------------------+-------------------------------------------+
'''
},
{
"name": "String in korean",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
키스의|고유조건은 입술끼리
만나야 하고 특별한|기술은 필요치 않다
''',
"output": u'''\
+--------------------+---------------------+
| 키스의             | 고유조건은 입술끼리 |
| 만나야 하고 특별한 | 기술은 필요치 않다  |
+--------------------+---------------------+
'''
},
{
"name": "String in russian",
"args": ["-b", "basic", "--col-separator", "|"],
"input": '''\
Съешь же ещё|этих мягких французских булок
да выпей|чаю
''',
"output": u'''\
+--------------+-------------------------------+
| Съешь же ещё | этих мягких французских булок |
| да выпей     | чаю                           |
+--------------+-------------------------------+
'''
},
]}
