#include "string_view.h"
#include <stdio.h>
#include <string.h>

void print_string_view(const String_view* string_view)
{
    for(size_t i = 0; i < string_view->size; ++i) {
        printf("%c", string_view->ptr[i]);
    }
}

String_view create_string_view(const char* data)
{
    String_view string_view;
    string_view.ptr = data;
    string_view.size = strlen(data);
    return string_view;
}
