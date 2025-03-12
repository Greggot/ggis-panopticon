#pragma once

#include "card.h"
#include "skird_config.h"
#include "string_view.h"
#include "user.h"

typedef struct {
    String_view title;
    const Card* parent;
    const Skird_config* config;
    String* tags_ptr;
    size_t tags_size;
} Create_paramters;

typedef enum {
    MEMBER = 1,
    OWNER = 2,
} Responsibility;

void create_card(const Env* env, const User*, const Create_paramters* creator);
