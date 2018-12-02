#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

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

struct ft_border_style * get_border_style(const char *str)
{
    struct ft_border_style *const border_styles[] = {
        FT_BASIC_STYLE,
        FT_BASIC2_STYLE,
        FT_SIMPLE_STYLE,
        FT_PLAIN_STYLE,
        FT_DOT_STYLE,
        FT_EMPTY_STYLE,
        FT_SOLID_STYLE,
        FT_SOLID_ROUND_STYLE,
        FT_NICE_STYLE,
        FT_DOUBLE_STYLE,
        FT_DOUBLE2_STYLE,
        FT_BOLD_STYLE,
        FT_BOLD2_STYLE,
        FT_FRAME_STYLE
    };

    const char * border_style_names[] = {
        "basic",
        "basic2",
        "simple",
        "plain",
        "dot",
        "empty",
        "solid",
        "solid_round",
        "nice",
        "double",
        "double2",
        "bold",
        "bold2",
        "frame",
    };
    unsigned i;

    const unsigned STYLES_NUMBER = sizeof(border_styles) / sizeof(border_styles[0]);

    for (i = 0; i <  STYLES_NUMBER; ++i) {
        if (strcmp(str, border_style_names[i]) == 0) {
            return border_styles[i];
        }
    }

    return NULL;
}


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


    struct ft_border_style *border_style = FT_EMPTY_STYLE;

    int opt;
    while ((opt = getopt(argc, argv, "b:")) != -1) {
        switch (opt) {
            case 'b':
                border_style = get_border_style(optarg);
                if (!border_style)
                    exit_with_error();// todo something    
                break;
            default:
                exit_with_error();// todo something
        }
    }


    ft_table_t *table = ft_create_table();
    if (table == NULL)
        exit_with_error();

    ft_set_border_style(table, border_style);

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
