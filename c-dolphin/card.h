#pragma once

#include "env.h"
#include "string.h"
#include "string_view.h"

typedef struct {
    int type_id;
    int condition;
    int offset;
    int limit;
    String_view query;
} Card_request;

String card_get_request(const Env*, const Card_request*);
