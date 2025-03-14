#pragma once

#include <stddef.h>

/// @brief Аналог std::string_view, ссылка на readonly-строку
typedef struct {
    const char* ptr;
    size_t size;
} String_view;

void print_string_view(const String_view*);
String_view create_string_view(const char*);
