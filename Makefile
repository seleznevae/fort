all: fort

LIBFORT_PATH=./libfort/lib
LIBFORT_SRC=${LIBFORT_PATH}/fort.c


fort: main.c
	${CC} -Wall -Wextra -Werror main.c ${LIBFORT_SRC} -I${LIBFORT_PATH} -o fort

clean:
	rm -f fort
