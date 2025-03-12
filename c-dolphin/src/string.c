#include "string.h"
#include "string_view.h"
#include <stdlib.h>
#include <string.h>

String create_string(const char* ptr)
{
    String string;
    string.size = strlen(ptr);
    string.ptr = (char*)malloc(string.size + 1);
    mempcpy(string.ptr, ptr, string.size);
    string.ptr[string.size] = 0;
    return string;
}

String allocate_string(size_t size)
{
    String string;
    string.size = size;
    string.ptr = (char*)malloc(string.size + 1);
    memset(string.ptr, 0, size + 1);
    return string;
}

void delete_string(String* string)
{
    free(string->ptr);
}

/// @todo destination empty case
void add_string(String* destination, const char* source)
{
    const size_t prev_size = destination->size;
    const size_t curr_size = strlen(source);
    destination->size += curr_size;
    destination->ptr = realloc(destination->ptr, destination->size + 1);
    mempcpy(destination->ptr + prev_size, source, curr_size);
    destination->ptr[destination->size] = 0;
}

/// @todo left empty case
String add_string_const_char(const String* left, const char* right)
{
    const size_t curr_size = strlen(right);
    String new_string = {
        .size = left->size + curr_size
    };

    new_string.ptr = (char*)malloc(new_string.size + 1);
    mempcpy(new_string.ptr, left->ptr, left->size);
    mempcpy(new_string.ptr + left->size, right, curr_size);
    new_string.ptr[new_string.size] = 0;
    return new_string;
}

String add_const_char_string(const char* left, const String* right)
{
    const size_t curr_size = strlen(left);
    String new_string = {
        .size = right->size + curr_size
    };

    new_string.ptr = (char*)malloc(new_string.size + 1);
    mempcpy(new_string.ptr, left, curr_size);
    mempcpy(new_string.ptr + curr_size, right->ptr, right->size);
    new_string.ptr[new_string.size] = 0;
    return new_string;
}

/// @todo destination empty case
void add_string_other(String* destination, const String* source)
{
    const size_t prev_size = destination->size;
    destination->size += source->size;
    destination->ptr = realloc(destination->ptr, destination->size + 1);
    mempcpy(destination->ptr + prev_size, source->ptr, source->size);
    destination->ptr[destination->size] = 0;
}

void add_string_to_string_view(String* string, const String_view* string_view)
{
    const size_t prev_size = string->size;
    string->size += string_view->size;
    string->ptr = realloc(string->ptr, string->size + 1);
    mempcpy(string->ptr + prev_size, string_view->ptr, string_view->size);
    string->ptr[string->size] = 0;
}

int string_contains_substring_view(const String* left, const String_view* right)
{
    if (right->size > left->size)
        return 0;

    for (size_t i = 0; i <= (left->size - right->size); ++i)
    {
        size_t j = 0;
        for (; j <= right->size; ++j) {
            if (left->ptr[i + j] != right->ptr[j])
                break;
        }
        if (j == right->size)
            return 1;
    }
    return 0;
}
