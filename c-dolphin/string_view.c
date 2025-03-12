#include "string_view.h"
#include <stdio.h>
#include <string.h>

void print(const String_view* string_view)
{
    printf("%.*s", (int)string_view->size, string_view->ptr);
}

String_view create_string_view(const char* data)
{
    String_view string_view;
    string_view.ptr = data;
    string_view.size = strlen(data);
    return string_view;
}
