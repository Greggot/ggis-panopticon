#include "user.h"
#include "string.h"
#include <cjson/cJSON.h>

User read_user(const char* json_str)
{
    cJSON* json = cJSON_Parse(json_str);
    cJSON* id = cJSON_GetObjectItem(json, "id");
    cJSON* full_name = cJSON_GetObjectItem(json, "full_name");
    cJSON* email = cJSON_GetObjectItem(json, "email");
    User user = {
        .id = id->valueint,
        .email = create_string(email->valuestring),
        .full_name = create_string(full_name->valuestring)
    };
    cJSON_Delete(json);
    return user;
}

void delete_user(User* user)
{
    delete_string(&user->email);
    delete_string(&user->full_name);
}
