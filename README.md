# fort - command line utility to create formatted tables

[![Build Status](https://travis-ci.org/seleznevae/fort.svg?branch=master)](https://travis-ci.org/seleznevae/fort)
[![Build Status](https://api.cirrus-ci.com/github/seleznevae/fort.svg)](https://cirrus-ci.com/github/seleznevae/fort)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Build

```bash
git clone https://github.com/seleznevae/fort && cd fort
git submodule init && git submodule update
mkdir build && cd build
cmake .. && make
```

## Usage examples

```bash
$ (printf "PERM LINKS OWNER GROUP SIZE MONTH DAY " ; \
   printf "HH:MM/YEAR NAME\n" ; \
   ls -l | sed 1d) | fort -b nice -s ' ' -m --header=0 --action='0bg-magenta'
```


## License

<img align="right" src="http://opensource.org/trademarks/opensource/OSI-Approved-License-100x137.png">

The class is licensed under the [MIT License](http://opensource.org/licenses/MIT):

Copyright &copy; 2018 - 2020 Seleznev Anton

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
