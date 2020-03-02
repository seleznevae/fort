#include <assert.h>
#include <ctype.h>
#include <errno.h>
#include <getopt.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

#include "fort.h"

static void exit_with_error(const char *message)
{
    fprintf(stderr, "fort: error: %s\n", message);
    exit(EXIT_FAILURE);
}

static void exit_with_sys_error()
{
    fprintf(stderr, "fort: error: %s\n", strerror(errno));
    exit(EXIT_FAILURE);
}

#define FORT_MAJOR_VERSION   0
#define FORT_MINOR_VERSION   1
#define FORT_BUGFIX_VERSION  0

#define BUFFER_SIZE (1 << 10)
#define MAX_BUFFER_SIZE (1 << 16)
#define COL_SEPARATOR ","
#define ROW_SEPARATOR "\n"

const struct ft_border_style * get_border_style(const char *str)
{
    const struct ft_border_style *const border_styles[] = {
        FT_BASIC_STYLE,
        FT_BASIC2_STYLE,
        FT_SIMPLE_STYLE,
        FT_PLAIN_STYLE,
        FT_DOT_STYLE,
        FT_EMPTY_STYLE,
        FT_EMPTY2_STYLE,
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
        "empty2",
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
    struct header_index *header_indexes = NULL;
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

struct action_item {
    struct action_item *next;
    /* Regex to match */
    regex_t regex;
    int re_set;
    /* Property to setup */
    int property;
    int property_value;
    /* Range of cells to match (both ends included) */
    long int row_beg;
    long int row_end;
};

enum ft_color string_to_color(const char *color, size_t sz)
{
    if (strncmp(color, "black", sz) == 0)
        return FT_COLOR_BLACK;
    if (strncmp(color, "red", sz) == 0)
        return FT_COLOR_RED;
    if (strncmp(color, "green", sz) == 0)
        return FT_COLOR_GREEN;
    if (strncmp(color, "yellow", sz) == 0)
        return FT_COLOR_YELLOW;
    if (strncmp(color, "blue", sz) == 0)
        return FT_COLOR_BLUE;
    if (strncmp(color, "magenta", sz) == 0)
        return FT_COLOR_MAGENTA;
    if (strncmp(color, "cyan", sz) == 0)
        return FT_COLOR_CYAN;

    exit_with_error("Ivalid color name");
    return FT_COLOR_DEFAULT;
}

static int string_to_option(const char *action, size_t *parsed)
{
    assert(action);
    assert(parsed);
    if (strstr(action, "fg-") == action) {
        *parsed = 3;
        return FT_CPROP_CONT_FG_COLOR;
    } else if (strstr(action, "bg-") == action) {
        *parsed = 3;
        return FT_CPROP_CELL_BG_COLOR;
    }

    exit_with_error("Ivalid action string");
    return 0;
}

static struct action_item *action_create()
{
    struct action_item *action = calloc(1, sizeof(struct action_item));
    if (!action)
        return action;
    action->row_beg = -1;
    action->row_end = -1;
    return action;
}

/* Format of action strings: "(range|/RE/|range/RE/)action" */
static void add_action_item(struct action_item **head, const char *action_str)
{
    const char RANGE_SEPARATOR = ',';

    size_t parsed = 0;
    size_t re_str_len = 0;
    char* re_str = NULL;
    const char *endptr = NULL;
    struct action_item *act = action_create();
    if (!act)
        exit_with_error("Not enough memory");

    if (strlen(action_str) == 0)
        exit_with_error("Ivalid format of match expession");

    /* Fill range if it is provided */
    if (isdigit(action_str[0])) {
        act->row_beg = strtol(action_str, (char **)&endptr, 10);
        if (endptr == action_str)
            exit_with_error("Ivalid format of match expession");
        act->row_end = act->row_beg;
        action_str = endptr;
        if (action_str[0] == RANGE_SEPARATOR) {
            ++action_str;
            act->row_end = strtol(action_str, (char **)&endptr, 10);
            if (endptr == action_str)
                exit_with_error("Ivalid format of match expession");
            action_str = endptr;
        }
    }

    /* Fill RE if it is provided */
    if (*action_str == '/') {
        ++action_str;
        endptr = action_str;
        again:
        while (*endptr && *endptr != '/') 
            endptr++;
        if (*endptr == '\0')
            exit_with_error("Ivalid format of match expession");
        // TODO: add processing of case when \ is escaped itself
        if (*(endptr - 1) == '\\') {
            endptr++;
            goto again;
        }

        re_str_len = endptr - action_str;
        re_str = malloc(re_str_len + 1);
        if (!re_str)
            exit_with_error("Not enough memory");
        re_str[re_str_len] = '\0';
        strncpy(re_str, action_str, re_str_len);

        if (regcomp(&act->regex, re_str, REG_NOSUB /* Do not report position of matches. */)) 
            exit_with_error("Invalid regular expression");
        action_str = endptr + 1;
        act->re_set = 1;
    }

    act->property = string_to_option(action_str, &parsed);
    action_str += parsed;
    act->property_value = string_to_color(action_str, strlen(action_str));
    
    act->next = *head;
    *head = act;
}

static void apply_action_if_match(ft_table_t *table, struct action_item *items_list, const char *str)
{
    size_t cur_row = ft_cur_row(table);

    struct action_item *item = items_list;
    while (item) {
        if (item->row_beg >= 0 && cur_row < (size_t)item->row_beg) 
            goto next;
        if (item->row_end >= 0 && cur_row > (size_t)item->row_end) 
            goto next;

        if (!item->re_set || !regexec(&item->regex, str, 0, NULL, 0)) {
            ft_set_cell_prop(table, FT_CUR_ROW, FT_CUR_COLUMN, item->property, item->property_value);
        }
    next:
        item = item->next;
    }
}

struct global_opts_t {
    const struct ft_border_style *border_style;
    int dummy;
    const char *col_separator;
    const char *row_separator;
    struct header_index *header_indexes;
    struct action_item *action_items;
    int ignore_empty_lines;
    int merge_empty_cells;
} global_opts;

static void free_options(struct global_opts_t *options)
{
    /* Free headers */
    struct header_index *hi = options->header_indexes;
    struct header_index *hi_next = NULL;
    while (hi) {
        hi_next = hi->next;
        free(hi);
        hi = hi_next;
    }
    options->header_indexes = NULL;

    /* Free match items */
    struct action_item *a = options->action_items;
    struct action_item *a_next = NULL;
    while (a) {
        a_next = a->next;
        regfree(&a->regex);
        free(a);
        a = a_next;
    }
    options->action_items = NULL;
}

static const char *opt_string = "a:b:ehms:S:v";

static void set_default_options()
{
    global_opts.border_style = FT_EMPTY_STYLE;
    global_opts.dummy = 0;
    global_opts.col_separator = COL_SEPARATOR;
    global_opts.row_separator = ROW_SEPARATOR;
    global_opts.header_indexes = NULL;
    global_opts.action_items = NULL;
    global_opts.ignore_empty_lines = 0;
    global_opts.merge_empty_cells = 0;
}

static int header_enabled = 0;

enum option_index {
    OPT_ACTION_INDEX = 0,
    OPT_BORDER_STYLE_INDEX,
    OPT_IGNORE_EMPTY_INDEX,
    OPT_HEADER_INDEX,
    OPT_HELP_INDEX,
    OPT_MERGE_EMPTY_CELL_INDEX,
    OPT_COL_SEPARATOR_INDEX,
    OPT_ROW_SEPARATOR_INDEX,
    OPT_VERSION_INDEX
};

static const struct option long_opts[] = {
    { "action", required_argument, NULL, 'a'},
    { "border-style", required_argument, NULL, 'b' },
    { "ignore-empty-lines", no_argument, NULL, 'e' },
    { "header", optional_argument, &header_enabled, 1},
    { "help", no_argument, NULL, 'h' },
    { "merge-empty-cell", no_argument, NULL, 'm' },
    { "col-separator", required_argument, NULL, 's' },
    { "row-separator", required_argument, NULL, 'S' },
    { "version", no_argument, NULL, 'v' },
};

const char HELP_STRING[] =
    "Usage: fort [OPTION]... [FILE]\n"
    "Convert input into formatted table.\n"
    "\n"
    "With no FILE, or when FILE is -, read standard input.\n"
    "\n"
    "  -a <action>, --action=<action>           apply action to cells of the output table\n"
    "  -b <style>, --border-style=<style>       border style of the output table\n"
    "  -e, --ignore-empty-lines                 ignore empty lines\n"
    "  --header=<n1>[,<n2>...]                  set row numbers that will be treated as headers\n"
    "  -h, --help                               print help and exit\n"
    "  -m, --merge-empty-cell                   merge empty cells\n"
    "  -s <set>, --col-separator=<set>          specify set of characters to be used to delimit columns\n"
    "  -S <set>, --row-separator=<set>          specify set of characters to be used to delimit rows\n"
    "  -v, --version                            output version information and exit\n";


char *get_next_line(FILE *fin, const char *sep_set)
{
    static size_t size = 1024;
    static size_t end_offset = 0;
    static size_t start_offset = 0;
    static char* cur_line = NULL;
    
    if (cur_line == NULL)
        cur_line = (char *)malloc(size + 1);

    if (cur_line == NULL)
        exit_with_error("Not enough memory"); 

    if (start_offset) {
        size_t n_remained = end_offset - start_offset;
        memmove(cur_line, cur_line + start_offset, n_remained);
        start_offset = 0;
        end_offset = n_remained;
        cur_line[end_offset] = '\0';
    }
    
    while (1) {
        /* Search for new_line */
        if (end_offset) {
            size_t nl_pos = strcspn (cur_line, sep_set);
            if (nl_pos < end_offset) {
                cur_line[nl_pos] = '\0';
                start_offset = nl_pos + 1;
                return cur_line;
            }
        }

        if (end_offset > size/2) {
            cur_line = (char *)realloc(cur_line, (size + 1) * 2);
            size *= 2;
        }
        if (cur_line == NULL)
            exit_with_error("Not enough memory"); 

        int n = fread(cur_line + end_offset, 1, (size - end_offset), fin);
        if (n == -1)
            exit_with_error("Error during input reading"); 
        if (n == 0) {
            if (end_offset == 0) {
                return NULL;
            } else {
                start_offset = end_offset;
                cur_line[end_offset] = '\0';
                return cur_line;
            }
        }

        end_offset += n;
        cur_line[end_offset] = '\0';
    }
}

int main(int argc, char *argv[])
{
    int status = EXIT_SUCCESS;
    FILE *fin;
    char *current_line = NULL;

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
            case 'a':
                add_action_item(&global_opts.action_items, optarg);
                break;
            case 'b':
                global_opts.border_style = get_border_style(optarg);
                if (!global_opts.border_style)
                    exit_with_error("Invalid border style");    
                break;
            case 'e':
                global_opts.ignore_empty_lines = 1;
                break;
            case 'z':
                printf("%s\n", optarg);
                return EXIT_SUCCESS;
                break;
            case 'h':
                printf(HELP_STRING);
                return EXIT_SUCCESS;
                break;
            case 'm':
                global_opts.merge_empty_cells = 1;
                break;
            case 's':
                global_opts.col_separator = optarg;
                break;
            case 'S':
                global_opts.row_separator = optarg;
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
    if (optind >= argc || strcmp(argv[optind], "-") == 0) {
        fin = stdin;
    } else {
        fin = fopen(argv[optind], "r");
        if (!fin) {
            exit_with_sys_error();
        }
    }

    while ((current_line = get_next_line(fin, global_opts.row_separator))) {
        if (global_opts.ignore_empty_lines && current_line[0] == '\0')
            continue;

        char *beg = current_line;
        char *end = current_line;
        while (1) {
            while (*end && strchr(global_opts.col_separator, *end) == NULL) {
                ++end;
            }
            if (beg == end && *end == '\0') {
                ft_ln(table);
                break;
            } else if (*end == '\0') {
                if (beg != end || !global_opts.merge_empty_cells) {
                    apply_action_if_match(table, global_opts.action_items, beg);
                    ft_u8write_ln(table, beg);
                } else {
                    ft_ln(table);
                }
                break;
            }
            *end = '\0';

            if (beg != end || !global_opts.merge_empty_cells) {
                apply_action_if_match(table, global_opts.action_items, beg);
                ft_u8write(table, beg);
            }

            ++end;
            beg = end;
        }
    }

    const char *str = (const char *)ft_to_u8string(table);
    if (str == NULL)
        exit_with_error("Internal error");
    printf("%s", str);

    ft_destroy_table(table);
    free_options(&global_opts);
    return status;
}
