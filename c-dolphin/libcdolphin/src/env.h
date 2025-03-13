#pragma once

#include "cd_string.h"

typedef struct {
    String kaiten_host;
    String kaiten_auth;
} Env;

Env read_env(const char* path);
void delete_env(Env*);
