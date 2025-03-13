#pragma once

#include "cd_string.h"

typedef struct {
    unsigned int id;
    String full_name; 
    String email;
} User;

User read_user(const char*);
void delete_user(User*);
