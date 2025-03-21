#pragma once

#include "string_view.h"
#include <stddef.h>

/// @brief Аналог std::string, ptr - C-style строка
typedef struct {
    char* ptr;
    size_t size;
} String;

String create_string(const char*);
String allocate_string(size_t);
void delete_string(String*);

void add_string_other(String*, const String*);
void add_string(String* destination, const char*);
String add_string_const_char(const String*, const char*);
String add_const_char_string(const char*, const String*);
void add_string_to_string_view(String*, const String_view*);

int string_contains_substring_view(const String* left, const String_view* right);
