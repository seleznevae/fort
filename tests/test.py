#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from subprocess import call, Popen, PIPE, STDOUT
import sys
import os

test_suites = []

from input_tests import input_test_suite
test_suites.append(input_test_suite)

from input_utf8_tests import input_utf8_test_suite
test_suites.append(input_utf8_test_suite)

from long_input_tests import long_input_test_suite
test_suites.append(long_input_test_suite)

from simple_tests import simple_test_suite
test_suites.append(simple_test_suite)

from merge_tests import merge_test_suite
test_suites.append(merge_test_suite)

from ignore_tests import ignore_test_suit
test_suites.append(ignore_test_suit)

from separator_tests import separator_test_suite
test_suites.append(separator_test_suite)

from row_separator_tests import row_separator_test_suite
test_suites.append(row_separator_test_suite)

from header_tests import header_test_suite
test_suites.append(header_test_suite)

from styles_tests import styles_test_suite
test_suites.append(styles_test_suite)

from actions_tests import action_test_suite
test_suites.append(action_test_suite)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run fort tests.')
    parser.add_argument('--bin-dir', help='Directory with fort executable')
    args = parser.parse_args()

    for test_suite in test_suites:
        print "Running {}".format(test_suite["name"])
        for test_case in test_suite["scenarios"]:
            print "  Executing {}".format(test_case["name"])
            if "beforeScript" in test_case:
                os.system(test_case["beforeScript"])

            process = Popen(["{}/fort".format(args.bin_dir)] + test_case["args"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
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
