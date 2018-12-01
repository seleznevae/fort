#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "fort.h"

static void exit_with_error()
{
    fprintf(stderr, "Internal libfort error\n");
    exit(EXIT_FAILURE);
}

#define BUFFER_SIZE (1 << 10)
#define MAX_BUFFER_SIZE (1 << 16)
#define COL_SEPARATOR '|'
#define NEW_LINE_CHAR '\n'

int main(int argc, char *argv[])
{
    (void)argc;
    (void)argv;

    int status = EXIT_SUCCESS;
    FILE *fin;
    int lin_sz = sizeof(char) * BUFFER_SIZE;
    char *current_line = malloc(lin_sz);
    if (current_line == NULL)
        exit_with_error();

    ft_table_t *table = ft_create_table();
    if (table == NULL)
        exit_with_error();

    ft_set_border_style(table, FT_BOLD2_STYLE);

    /* Reading input file */
    fin = stdin;
    while (fgets(current_line, lin_sz, fin)) {
        // printf("READ line(%d):%s", (int)strlen(current_line), current_line);
        char *beg = current_line;
        char *end = current_line;
        while (1) {
            while (*end && *end != COL_SEPARATOR) {
                ++end;
            }
            if (beg == end) {
                ft_ln(table);
                break;
            } else if (*end == '\0') {
                if (*(end - 1) == NEW_LINE_CHAR) {
                    --end;
                    *end = '\0';
                }
                ft_write_ln(table, beg);
                break;
            }
            *end = '\0';
            ft_write(table, beg);
            ++end;
            beg = end;
        }
    }

    const char *str = ft_to_string(table);
    if (str == NULL)
        exit_with_error();

    printf("%s", str);


    ft_destroy_table(table);

    return status;
}
