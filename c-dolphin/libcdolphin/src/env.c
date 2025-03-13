#include "env.h"
#include "cd_string.h"
#include "file.h"
#include <cjson/cJSON.h>
#include <stdio.h>
#include <stdlib.h>

/// @brief Считать хост Кайтена и преобразовать токен в заголовок HTTPS,
/// сам по себе токен больше никому и не нужен, его нет смысла хранить
Env read_env(const char* path)
{
    String json_string = read_file_string(path);
    cJSON* json = cJSON_Parse(json_string.ptr);
    cJSON* host = cJSON_GetObjectItem(json, "kaiten_host");
    cJSON* token = cJSON_GetObjectItem(json, "kaiten_token");

    Env env = {
        .kaiten_host = create_string(host->valuestring),
    };

    static const char* format = "Authorization: Bearer %s";
    int length = snprintf(NULL, 0, format, token->valuestring);
    env.kaiten_auth.size = length + 1;
    env.kaiten_auth.ptr = (char*)malloc(env.kaiten_auth.size);
    snprintf(env.kaiten_auth.ptr, length + 1, format, token->valuestring);

    cJSON_Delete(json);
    delete_string(&json_string);
    return env;
}

void delete_env(Env* env)
{
    delete_string(&env->kaiten_host);
    delete_string(&env->kaiten_auth);
}
