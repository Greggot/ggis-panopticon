#pragma once

#include "string.h"

typedef struct {
    String id_19;
} Magic_properties;

typedef struct {
    unsigned int board_id;
    unsigned int column_id;
    unsigned int lane_id;
    String size_text;
    unsigned int type_id;
    Magic_properties magic_properties;
} Skird_config;

Skird_config read_skird_config(const char*);
void delete_skird_config(Skird_config*);
