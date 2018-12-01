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
TEST_CASE="SIMPLE TAST CASE"

./fort > ${TMP_FILE} <<DATA
1|3
4|5
DATA

diff ${TMP_FILE} - >/dev/null  2>/dev/null <<ETALON
┏━━━┯━━━┓
┃ 1 │ 3 ┃
┠───┼───┨
┃ 4 │ 5 ┃
┗━━━┷━━━┛
ETALON

check_test_result $? ${TEST_CASE}
###########################################################

rm ${TMP_FILE}
if [ "$ALL_TESTS_PASSED" = "1" ]; then
    echo -e "\e[32mALL TESTS PASSED\e[0m"
else
    exit 1
fi
