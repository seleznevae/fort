CFLAGS    += -g3 -Wall -Wextra -Werror
INCFLAGS  =

RONN := ronn
BIN  := fort
DOCS := ./docs/fort.1 ./docs/fort.1.html

SRC  := main.c
HDRS := 

LIBFORT_PATH   = ./libfort/lib
LIBFORT_SRC    = ${LIBFORT_PATH}/fort.c
LIBFORT_HDR    = ${LIBFORT_PATH}/fort.h
LIBFORT_CFLAGS = -DFT_CONGIG_DISABLE_WCHAR

CFLAGS   += ${LIBFORT_CFLAGS}
SRC      += ${LIBFORT_SRC}
HDRS     += ${LIBFORT_HDR}
INCFLAGS += -I${LIBFORT_PATH}

$(BIN): ${SRC} ${HDRS}
	${CC} ${CFLAGS} ${SRC} ${INCFLAGS} -o $(BIN)


RONN_DEFINED := $(shell command -v ${RONN} 2> /dev/null)
ifndef RONN_DEFINED
$(warning "`${RONN}` utility is not found. Generation of docs is disabled.")
DOCS = 
else
$(DOCS): docs/fort.md
	ronn ./docs/fort.md
endif
docs: $(DOCS)

test: $(BIN) 
	cd tests ; ./test.py 

all: $(BIN) docs test

clean:
	$(RM) -rf $(BIN) $(DOCS)


.PHONY: all clean test