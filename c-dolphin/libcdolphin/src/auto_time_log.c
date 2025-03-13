#include "auto_time_log.h"
#include "card.h"
#include "cd_string.h"
#include "date.h"
#include "env.h"
#include "file.h"
#include "kaiten_endpoint.h"
#include "requests.h"
#include <cjson/cJSON.h>
#include <stdio.h>
#include <string.h>

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
        .start_date = date_from_string(start_date->valuestring),
        .days_count = days_count->valueint,
        .time_spent_min = time_spent->valueint,
        .role_id = role_id->valueint,
        .card_id = card_id->valueint
    };
    cJSON_Delete(json);
    delete_string(&data);
    return config;
}

int iterate_date_skip_weekends(Date* date, int i, int max)
{
    if (date->day < 10)
        printf("[ %u] ", date->day);
    else
        printf("[%u] ", date->day);
    next_day(&date->day, &date->month, &date->year);
    if (++i == max)
        return 1;

    if (is_day_off(date)) {
        printf(" [X] ");
        next_day(&date->day, &date->month, &date->year);
        if (++i == max)
            return 1;
        printf(" [X]\n");
        next_day(&date->day, &date->month, &date->year);
        if (++i == max)
            return 1;

        if (date->day < 2) {
            printf("\n%s\n", month_name(date->month));
        }
        return 1;
    }

    if (date->day == 1)
        printf("\n%s\n", month_name(date->month));
    return 0;
}

int iterate_date_skip_weekends_silent(Date* date)
{
    next_day(&date->day, &date->month, &date->year);
    if (is_day_off(date)) {
        next_day(&date->day, &date->month, &date->year);
        next_day(&date->day, &date->month, &date->year);
        return 1;
    }
    return 0;
}

String serialize_time_log_config(const Time_log_config* config)
{
    static char date[10];
    cJSON* root = cJSON_CreateObject();

    cJSON_AddNumberToObject(root, "role_id", config->role_id);
    cJSON_AddNumberToObject(root, "time_spent", config->time_spent_min);
    date_to_string(date, &config->start_date);
    cJSON_AddStringToObject(root, "for_date", date);

    String json;
    json.ptr = cJSON_Print(root);
    json.size = strlen(json.ptr);

    cJSON_Delete(root);
    return json;
}

void register_time(const Env* env, const Time_log_config* config)
{
    String time_log_url = kaiten_card_time_logs_url(env, config->card_id);
    String json = serialize_time_log_config(config);
    String answer = request_post(env, &time_log_url, &json);

    delete_string(&answer);
    delete_string(&json);
    delete_string(&time_log_url);
}

void what_write_time_log_gonna_do(const Env* env, const Time_log_config* config)
{
    Date date = config->start_date;
    printf("Списать по %u минут в даты (%u): \n", config->time_spent_min, date.year);

    printf("%s\n", month_name(date.month));

    for (size_t i = 0; i < config->days_count; ++i)
        if (iterate_date_skip_weekends(&date, i, config->days_count))
            i += 2;

    Card card = card_by_id(env, config->card_id);
    printf("\nCARD: %s\n", card.title.ptr);
    delete_string(&card.title);
}

void write_time_log(const Env* env, Time_log_config* config)
{
    for (size_t i = 0; i < config->days_count; ++i) {
        register_time(env, config);
        if (iterate_date_skip_weekends_silent(&config->start_date))
            i += 2;
    }
}
