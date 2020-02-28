#!/usr/bin/env python
# -*- coding: utf-8 -*-


big_string_1 = 'a'*56784 + '1'
big_string_2 = 'a'*56783 + '2'
big_string_3 = 'a'*56783 + '3'
big_string_4 = 'a'*56784 + '4'
long_input_test_suite = {
"name": "Long input tests",
"scenarios": [
{
"name": "long input",
"args": ["--col-separator", "|"],
"input": '{}|{}\n{}|{}'.format(big_string_1,big_string_2,big_string_3,big_string_4) ,
"output": ' {}  {}  \n {}   {} \n'.format(big_string_1,big_string_2,big_string_3,big_string_4) 
}
]}