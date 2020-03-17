fort(1) -- convert input into formatted table
=============================================

## SYNOPSIS

`fort` [<OPTION>...] [<FILE>]...

## DESCRIPTION

Fort converts its input into the formatted text table.

With no FILE, or when FILE is -, read standard input.

The input is broken into lines, default line separator is "\n", and lines are broken into fields, default field separator is ",". Fields content is then inserted into the cells of the resulting table. All lines of the input are threated equally. To make a particular line emphasized like a header use `--header` option.

## OPTIONS
  * `-a` <action>, `--action`=<action>:
    Apply action on cells of the output table. Format of actions:
    "(range|/RE/|range/RE/)action"

    Examples of setting actions:

    `--action=0magenta` # colorize in magenta cells in the 0th row

    `--action=1-3green` # colorize in green cells in range from 1st row to 3rd row (both ends included)

    `--action=/go*gle/red` # colorize in red cells that match regex 'go*gle'

    `--action=3,5/go*gle/yellow` # colorize in yellow cells in range from 3rd row to 5th row (both ends included) that match regex 'go*gle'

  * `-b` <name>, `--border`=<name>:
    Set border style of the output table. Available border style names: *basic*, *basic2*, *simple*, *plain*, *dot*, *empty* (default style), *empty2*, *solid*, *solid_round*, *nice*, *double*, *double2*, *bold*, *bold2*, *frame*.
  
  * `-e`, `--ignore-empty-lines`:
    Ignore empty lines in input.

  * `--header`=<n1>[,<n2>...]:
    Set row numbers that will be treated as headers.

  * `-h`, `--help`:
    Display help and exit.

  * `-m`, `--merge-empty-cells`:
    By default, fort will print empty cells as they are and will not merge adjacent delimeters into a single one; this option disables this behavior.

  * `-s` <SET>, `--col-separator`=<SET>:
    Specify set of characters to be used as column delimeters. Default column delimeters set is ','.

  * `-S` <SET>, `--row-separator`=<SET>:
    Specify set of characters to be used as row delimeters. Default column delimeters set is '\n'.

  * `-v`, `--version`:
    Display version information and exit.

## EXAMPLES


## AUTHOR

Written by Anton Seleznev.

## COPYRIGHT

Copyright (C) 2018-2020 Anton Seleznev.
License MIT <https://opensource.org/licenses/MIT>.

## SEE ALSO

awk(1), colrm(1), column(1), paste(1)
