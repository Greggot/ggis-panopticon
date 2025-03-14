#pragma once

#include "date.h"
#include "env.h"

typedef enum {
    DEVELOPER = 3,
} Role_id;

typedef struct {
    Date start_date;
    unsigned int days_count;
    unsigned int time_spent_min;
    Role_id role_id;
    int card_id;
} Time_log_config;

Time_log_config read_time_log_config(const char* path);
void write_time_log(const Env* env, Time_log_config*);
void what_write_time_log_gonna_do(const Env* env, const Time_log_config*);
