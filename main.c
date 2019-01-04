#include <errno.h>
#include <getopt.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <wchar.h>
#include <locale.h>
#include <iconv.h>
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
#define COL_SEPARATOR "|"
#define ROW_SEPARATOR "\n"

struct ft_border_style * get_border_style(const char *str)
{
    struct ft_border_style *const border_styles[] = {
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
    const char *col_separator;
    const char *row_separator;
    struct header_index *header_indexes;
} global_opts;

static const char *opt_string = "b:hn:s:v";

void set_default_options()
{
    global_opts.border_style = FT_EMPTY_STYLE;
    global_opts.dummy = 0;
    global_opts.col_separator = COL_SEPARATOR;
    global_opts.row_separator = ROW_SEPARATOR;
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
    { "new-line-separator", required_argument, NULL, 'n' },
    { "separator", required_argument, NULL, 's' },
    { "version", no_argument, NULL, 'v' },
};

const char HELP_STRING[] =
    "Usage: fort [OPTION]... [FILE]\n"
    "Format input into formatted table.\n"
    "\n"
    "With no FILE, or when FILE is -, read standard input.\n"
    "\n"
    "  -b <style>, --border-style=<style>       border style of the output table\n"
    "  --header=<n1>[,<n2>...]                  set row numbers that will be treated as headers\n"
    "  -h, --help                               print help and exit\n"
    "  -n <set>, --new-line-separator=<set>     specify set of characters to be used to delimit rows\n"
    "  -s <set>, --separator=<set>              specify set of characters to be used to delimit columns\n"
    "  -v, --version                            output version information and exit\n";


#ifdef FT_HAVE_WCHAR
wchar_t *utf8_str_to_wchar_str(char *beg, char *end)
{
    iconv_t cd = iconv_open("WCHAR_T", "UTF-8");
    if (cd == (iconv_t)-1) {
        exit_with_error("internal error: iconv_open");
    }

    char *inbuf = beg;
    size_t inbytesleft = end - beg;

    static wchar_t *wchar_str = NULL;
    static size_t sz = 0;
    if (wchar_str == NULL || sz < inbytesleft) {
        sz = 2 * inbytesleft + 1; /* multiply by 2 - for safety */
        wchar_str = malloc(sz * sizeof(wchar_t));
        if (wchar_str == NULL)
            exit_with_error("Not enough memory");
    }
    memset((void*)wchar_str, 0, sz * sizeof(wchar_t));
    char *outbuf = (char*)wchar_str;
    size_t outbytesleft = sz * sizeof(wchar_t);

    size_t ir = iconv(cd, &inbuf, &inbytesleft, &outbuf, &outbytesleft);
    if (ir == (size_t)-1) {
        exit_with_error("internal error: iconv");
    }
    if (inbytesleft) {
        exit_with_error("internal error: iconv in bytes left");
    }
    
    iconv_close(cd);
    return wchar_str;
}
#endif


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
                global_opts.col_separator = optarg;
                break;
            case 'n':
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
        char *beg = current_line;
        char *end = current_line;
        while (1) {
            while (*end && strchr(global_opts.col_separator, *end) == NULL) {
                ++end;
            }
            if (beg == end) {
                ft_ln(table);
                break;
            } else if (*end == '\0') {
#ifdef FT_HAVE_WCHAR
                ft_wwrite_ln(table, utf8_str_to_wchar_str(beg, end));
#else
                ft_write_ln(table, beg);
#endif
                break;
            }
            *end = '\0';
#ifdef FT_HAVE_WCHAR
            ft_wwrite(table, utf8_str_to_wchar_str(beg, end));
#else
            ft_write(table, beg);
#endif
            ++end;
            beg = end;
        }
    }


#ifdef FT_HAVE_WCHAR
    setlocale(LC_CTYPE, "");
    /* Convert table to string and print */
    const wchar_t *str = ft_to_wstring(table);
    if (str == NULL)
        exit_with_error("Internal error");
    fwprintf(stdout, L"%ls", str);
#else
    /* Convert table to string and print */
    const char *str = ft_to_string(table);
    if (str == NULL)
        exit_with_error("Internal error");
    printf("%s", str);
#endif

    ft_destroy_table(table);

    return status;
}
