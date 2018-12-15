#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <getopt.h>

#include "fort.h"

static void exit_with_error(const char *message)
{
    fprintf(stderr, "fort: error: %s\n", message);
    exit(EXIT_FAILURE);
}

#define FORT_MAJOR_VERSION   0
#define FORT_MINOR_VERSION   1
#define FORT_BUGFIX_VERSION  0

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

struct header_index {
    int index;
    struct header_index *next;
};

static struct header_index * set_header_indexes(char *indexes_str)
{
    struct header_index *header_indexes;
    if (indexes_str == NULL) {
        header_indexes = (struct header_index *)malloc(sizeof(struct header_index));
        header_indexes->index = 0;
        header_indexes->next = NULL;
    } else {
        char *strtok(char *string, const char *delim);
        const char *str = strtok(indexes_str, ",");
        while (str) {
            char *endptr = NULL;
            int index = strtoll (str, &endptr, 10);
            if (*endptr != '\0') {
                exit_with_error("Invalid header row number");  
                // exit_with_error("Invalid header row number: %s", str);  
            }
            struct header_index * new_header_index = (struct header_index *)malloc(sizeof(struct header_index));
            new_header_index->index = index;
            new_header_index->next = header_indexes;
            header_indexes = new_header_index;
            str = strtok(NULL, ",");
        }
    }
    return header_indexes;
}

struct global_opts_t {
    struct ft_border_style *border_style;
    int dummy;
    char col_separator;
    struct header_index *header_indexes;
} global_opts;

static const char *opt_string = "b:hs:v";

void set_default_options()
{
    global_opts.border_style = FT_EMPTY_STYLE;
    global_opts.dummy = 0;
    global_opts.col_separator = COL_SEPARATOR;
    global_opts.header_indexes = NULL;
}

static int header_enabled = 0;


#define OPT_BORDER_STYLE_INDEX    0
#define OPT_HEADER_INDEX          1
#define OPT_HELP_INDEX            2
#define OPT_SEPARATOR_INDEX       3
#define OPT_VERSION_INDEX         4

static const struct option long_opts[] = {
    { "border-style", required_argument, NULL, 'b' },
    { "header", optional_argument, &header_enabled, 1},
    { "help", no_argument, NULL, 'h' },
    { "separator", required_argument, NULL, 's' },
    { "version", no_argument, NULL, 'v' },
};

const char HELP_STRING[] =
    "Usage: fort [OPTION]... [FILE]\n"
    "Formats its input into formatted table.\n"
    "\n"
    "With no FILE, or when FILE is -, read standard input.\n"
    "\n"
    "  -b, --border-style     border style of the output table\n"
    "  --header               set row numbers that will be treated as headers\n"
    "  -h, --help             print help\n"
    "  -s, --separator        set field separator char of input file\n"
    "  -v, --version          output version information and exit\n";

int main(int argc, char *argv[])
{
    int status = EXIT_SUCCESS;
    FILE *fin;
    int lin_sz = sizeof(char) * BUFFER_SIZE;
    char *current_line = malloc(lin_sz);
    if (current_line == NULL)
        exit_with_error("Internal error");

    set_default_options();

    /* Reading options */
    int opt;
    int longindex;
    while ((opt = getopt_long(argc, argv, opt_string, long_opts, &longindex)) != -1) {
        switch (opt) {
            case 0:
                if (longindex == OPT_HEADER_INDEX) {
                    global_opts.header_indexes = set_header_indexes(optarg);
                } else {
                    exit_with_error("Invalid option"); 
                }
                break;
            case 'b':
                global_opts.border_style = get_border_style(optarg);
                if (!global_opts.border_style)
                    exit_with_error("Invalid border style");    
                break;
            case 'z':
                printf("%s\n", optarg);
                return EXIT_SUCCESS;
                break;
            case 'h':
                printf(HELP_STRING);
                return EXIT_SUCCESS;
                break;
            case 's':
                if (strlen(optarg) != 1)
                    exit_with_error("Invalid separator");  
                global_opts.col_separator = optarg[0];
                break;
            case 'v':
                printf("fort %d.%d.%d\n", FORT_MAJOR_VERSION, FORT_MINOR_VERSION, FORT_BUGFIX_VERSION);
                return EXIT_SUCCESS;
                break;

            default:
                exit_with_error("unrecognized arguments:"); //todo: add print unrecognised args
        }
    }

    ft_table_t *table = ft_create_table();
    if (table == NULL)
        exit_with_error("Internal error");

    ft_set_border_style(table, global_opts.border_style);

    while (global_opts.header_indexes) {
        ft_set_cell_prop(table, global_opts.header_indexes->index, FT_ANY_COLUMN, FT_CPROP_ROW_TYPE, FT_ROW_HEADER);
        global_opts.header_indexes = global_opts.header_indexes->next;
    }

    /* Reading input file */
    fin = stdin;
    while (fgets(current_line, lin_sz, fin)) {
        char *beg = current_line;
        char *end = current_line;
        while (1) {
            while (*end && *end != global_opts.col_separator) {
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



    /* Convert table to string and print */
    const char *str = ft_to_string(table);
    if (str == NULL)
        exit_with_error("Internal error");
    printf("%s", str);

    ft_destroy_table(table);

    return status;
}
