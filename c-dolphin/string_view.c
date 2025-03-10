#include "string_view.h"
#include <stdio.h>

void print(const String_view* string_view)
{
    printf("%.*s", (int)string_view->size, string_view->ptr);
}
