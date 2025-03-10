#pragma once

#include <stddef.h>

/// @brief Аналог std::string_view, ссылка на readonly-строку
typedef struct {
    const char* ptr;
    size_t size;
} String_view;

void print(const String_view*);
