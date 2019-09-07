all: fort

LIBFORT_PATH=./libfort/lib
LIBFORT_SRC=${LIBFORT_PATH}/fort.c
LIBFORT_HDR=${LIBFORT_PATH}/fort.h


fort: main.c ${LIBFORT_SRC} ${LIBFORT_HDR}
	${CC} -DFT_CONGIG_DISABLE_WCHAR -g3 -Wall -Wextra -Werror main.c ${LIBFORT_SRC} -I${LIBFORT_PATH} -o fort

clean:
	rm -f fort
