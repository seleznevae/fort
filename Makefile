all: fort

fort: main.c
	gcc -Wall -Wextra -Werror main.c fort.c -o fort
