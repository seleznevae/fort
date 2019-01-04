fort(1) -- format input into formatted table
=============================================

## SYNOPSIS

`fort` [<OPTION>...] [<FILE>]...

## DESCRIPTION

Fort converts its input into the formatted text table.

With no FILE, or when FILE is -, read standard input.

The input is broken into lines, default line separator = "\n", and lines are broken into fields, default field separator = "|". Fields content is then inserted into the cells of the resulting table.

All lines of the input are threated equally. To 


A normal paragraph. This can span multiple lines and is terminated with two
or more line endings -- just like Markdown.

Inline markup for `code`, `user input`, and **strong** are displayed
boldface; <variable>, _emphasis_, *emphasis*, are displayed in italics
(HTML) or underline (roff).

Manual references like sh(1), markdown(7), roff(7), etc. are hyperlinked in
HTML output.

Link to sections like [STANDARDS][], [SEE ALSO][], or [WITH A DIFFERENT LINK
TEXT][#SEE-ALSO].

Definition lists:

  * `-a`, `--argument`=[<value>]:
    One or more paragraphs describing the argument.

  * You can put whatever you *want* here, really:
    Nesting and paragraph spacing are respected.

Frequently used sections:

## OPTIONS
  * `-b` <name>, `--border-style`=<name>:
    Set border style of the output table. Available border style names: **basic**, **basic2**, **simple**, **plain**, **dot**, **empty** (default style), **empty2**, **solid**, **solid_round**, **nice**, **double**,      **double2**, **bold**, **bold2**, **frame**.
  
  * `--header`=<n1>[,<n2>...]:
    Set row numbers that will be treated as headers.

  * `-h`, `--help`:
    Display help and exit.

  * `-n` <SET>, `--new-line-separator`=<SET>:
    Specify set of characters to be used as row delimeters.

  * `-s` <SET>, `--separator`=<SET>:
    Specify set of characters to be used as field delimeters.

  * `-v`, `--version`:
    Display version information and exit.

  * You can put whatever you *want* here, really:
    Nesting and paragraph spacing are respected.
## SYNTAX
## ENVIRONMENT
## RETURN VALUES
## STANDARDS
## SECURITY CONSIDERATIONS
## BUGS
## HISTORY
## AUTHOR

Written by Anton Seleznev.

## COPYRIGHT

Copyright (C) 2018 Anton Seleznev
License MIT ???

## SEE ALSO

ronn-format(7), manpages(5), man(1), roff(7), groff(1), markdown(7)
change this list!!