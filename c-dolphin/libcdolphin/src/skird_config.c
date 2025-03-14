#include "skird_config.h"
#include "file.h"
#include "cd_string.h"
#include <cjson/cJSON.h>

Skird_config read_skird_config(const char* path)
{
    String json_string = read_file_string(path);
    cJSON* json = cJSON_Parse(json_string.ptr);
    cJSON* board_id = cJSON_GetObjectItem(json, "board_id");
    cJSON* column_id = cJSON_GetObjectItem(json, "column_id");
    cJSON* lane_id = cJSON_GetObjectItem(json, "lane_id");
    cJSON* size_text = cJSON_GetObjectItem(json, "size_text");
    cJSON* type_id = cJSON_GetObjectItem(json, "type_id");
    cJSON* properties = cJSON_GetObjectItem(json, "properties"); 
    cJSON* id_19 = cJSON_GetObjectItem(properties, "id_19"); 

    Skird_config config = {
        .board_id = board_id->valueint, 
        .column_id = column_id->valueint, 
        .lane_id = lane_id->valueint, 
        .size_text = create_string(size_text->valuestring), 
        .type_id = type_id->valueint, 
        .magic_properties.id_19 = create_string(id_19->valuestring),
    };
    cJSON_Delete(json);
    delete_string(&json_string);
    return config;
}

void delete_skird_config(Skird_config* config) 
{ 
    delete_string(&config->size_text);
    delete_string(&config->magic_properties.id_19);
}
