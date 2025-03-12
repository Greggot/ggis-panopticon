#include "env.h"
#include "string.h"
#include <cjson/cJSON.h>
#include <stdio.h>
#include <stdlib.h>

static String read_json(const char* path)
{
    String string = { .ptr = NULL, .size = 0 };
    FILE* file = fopen(path, "r");

    if (file == NULL) {
        printf("Cannot read file \"%s\"", path);
        return string;
    }

    fseek(file, 0, SEEK_END);
    string.size = ftell(file);
    fseek(file, 0, SEEK_SET);

    string.ptr = (char*)malloc(string.size + 1);
    if (string.ptr == NULL) {
        printf("Cannot allocate text_data");
        string.size = 0;
        return string;
    }

    fread(string.ptr, string.size, 1, file);
    fclose(file);
    
    string.ptr[string.size] = 0;
    ++string.size;
    return string;
}

Env read_env(const char* path)
{
    String json_string = read_json(path);
    cJSON* json = cJSON_Parse(json_string.ptr);
    cJSON* host = cJSON_GetObjectItem(json, "kaiten_host");
    cJSON* token = cJSON_GetObjectItem(json, "kaiten_token");
    Env env = {
        .kaiten_host = create_string(host->valuestring),
        .kaiten_token = create_string(token->valuestring)
    };
    cJSON_Delete(json);
    delete_string(&json_string);
    return env;
}

void delete_env(Env* env)
{
    delete_string(&env->kaiten_host);
    delete_string(&env->kaiten_token);
}
