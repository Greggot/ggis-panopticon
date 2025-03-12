#include "string.h"
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
    destination->ptr = realloc(destination->ptr, destination->size);
    mempcpy(destination->ptr + prev_size - 1, source, curr_size);
}

/// @todo left empty case
String add_string_const(const String* left, const char* right)
{
    const size_t curr_size = strlen(right);
    String new_string = {
        .size = left->size + curr_size
    };
    new_string.ptr = (char*)malloc(new_string.size);
    mempcpy(new_string.ptr, left->ptr, left->size);
    mempcpy(new_string.ptr + left->size - 1, right, curr_size);
    return new_string;
}

/// @todo destination empty case
void add_string_other(String* destination, const String* source) 
{ 
    const size_t prev_size = destination->size;
    destination->size += source->size;
    destination->ptr = realloc(destination->ptr, destination->size);
    mempcpy(destination->ptr + prev_size - 1, source->ptr, source->size);
}
