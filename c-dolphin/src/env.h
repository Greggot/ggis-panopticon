#pragma once

#include "string.h"

typedef struct {
    String kaiten_host;
    String kaiten_token;
} Env;

Env read_env(const char* path);
void delete_env(Env*);
