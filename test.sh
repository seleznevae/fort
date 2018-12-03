#!/bin/bash

ALL_TESTS_PASSED=1

function check_test_result() 
{
    if [ "$1" != "0" ]; then
        ALL_TESTS_PASSED=0
        echo -e "\e[31mTest case $2 failed\e[0m"
    fi
}

TMP_FILE=tmp_XXX

##########################################################
TEST_CASE="SIMPLE TEST CASE"

./fort -b basic > "${TMP_FILE}" <<DATA
1|3
4|5
DATA

diff "${TMP_FILE}" - >/dev/null  2>/dev/null <<ETALON
+---+---+
| 1 | 3 |
| 4 | 5 |
+---+---+
ETALON

check_test_result $? "${TEST_CASE}"
##########################################################
TEST_CASE="SIMPLE TEST CASE 2"

./fort -b basic > "${TMP_FILE}" <<DATA
1|3|5

4|5
1|22|33|66
DATA

diff "${TMP_FILE}" -  <<ETALON
+---+----+----+----+
| 1 | 3  | 5  |    |
|   |    |    |    |
| 4 | 5  |    |    |
| 1 | 22 | 33 | 66 |
+---+----+----+----+
ETALON

check_test_result $? "${TEST_CASE}"
##########################################################
TEST_CASE="SIMPLE SEPARATOR TEST CASE"

./fort -b basic -s % > "${TMP_FILE}" <<DATA
1%3
4%5
DATA

diff "${TMP_FILE}" - >/dev/null  2>/dev/null <<ETALON
+---+---+
| 1 | 3 |
| 4 | 5 |
+---+---+
ETALON

check_test_result $? "${TEST_CASE}"
###########################################################

rm ${TMP_FILE}
if [ "$ALL_TESTS_PASSED" = "1" ]; then
    echo -e "\e[32mALL TESTS PASSED\e[0m"
else
    exit 1
fi
