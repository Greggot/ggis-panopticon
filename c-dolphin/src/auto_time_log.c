#include "auto_time_log.h"
#include "env.h"
#include "file.h"
#include "requests.h"
#include "string.h"
#include <cjson/cJSON.h>
#include <stdio.h>

Time_log_config read_time_log_config(const char* path)
{
    String data = read_file_string(path);
    cJSON* json = cJSON_Parse(data.ptr);
    cJSON* start_date = cJSON_GetObjectItem(json, "start_date");
    cJSON* days_count = cJSON_GetObjectItem(json, "days_count");
    cJSON* time_spent = cJSON_GetObjectItem(json, "time_spent");
    cJSON* role_id = cJSON_GetObjectItem(json, "role_id");
    cJSON* card_id = cJSON_GetObjectItem(json, "card_id");

    Time_log_config config = {
        .start_date = create_string(start_date->valuestring),
        .days_count = days_count->valueint,
        .time_spent_min = time_spent->valueint,
        .role_id = role_id->valueint,
        .card_id = card_id->valueint
    };
    cJSON_Delete(json);
    delete_string(&data);
    return config;
}

int is_day_off(const Env* env, const String* date) 
{
    String url = create_string("https://isdayoff.ru/YYYY-MM-DD");
    char* ptr = url.ptr + 20;
    char* other = date->ptr;
    for(int i = 0; i < 10; ++i) {
        *(ptr++) = *(other++);
    }
    String answer = request_dayoff_get(&url);

    printf("Date request: %s\n", url.ptr);
    printf("Answer: %s\n", answer.ptr);

    delete_string(&url);
    delete_string(&answer);
    return 0;
}

void write_time_log(const Env* env, const Time_log_config* config)
{
    is_day_off(env, &config->start_date);
}
