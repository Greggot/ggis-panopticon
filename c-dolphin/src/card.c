#include "card.h"
#include "kaiten_endpoint.h"
#include "string.h"
#include <cjson/cJSON.h>
#include <stdio.h>
#include <stdlib.h>

String card_get_request(const Env* env, const Card_request* request)
{
    static const char* format = "?type_id=%i&condition=%i&offset=%i&limit=%i&query=\"%.*s\"";
    int length = snprintf(NULL, 0,
        format,
        request->type_id, request->condition, request->offset,
        request->limit, (int)request->query.size, request->query.ptr);

    String url = kaiten_cards_url(env);
    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1, format,
        request->type_id, request->condition, request->offset,
        request->limit, (int)request->query.size, request->query.ptr);
    return url;
}

Card_array read_cards(const char* data)
{
    Card_array card_array = {
        .card_ptr = NULL,
        .size = 0
    };
    cJSON* json = cJSON_Parse(data);
    card_array.size = cJSON_GetArraySize(json);
    if (card_array.size <= 0) {
        card_array.size = 0;
        cJSON_Delete(json);
        return card_array;
    }

    card_array.card_ptr = (Card*)malloc(sizeof(Card) * card_array.size);
    for (int i = 0; i < card_array.size; ++i)
    {
        cJSON* card_object = cJSON_GetArrayItem(json, i);
        cJSON* id = cJSON_GetObjectItem(card_object, "id");
        cJSON* title = cJSON_GetObjectItem(card_object, "title");
        cJSON* properties = cJSON_GetObjectItem(card_object, "properties");
        cJSON* sprint = cJSON_GetObjectItem(properties, "id_12");

        Card card = {
            .id = id->valueint,
            .sprint = (sprint == NULL) ? 0 : sprint->valueint,
            .title = create_string(title->valuestring),
        };
        card_array.card_ptr[i] = card;
    };
    cJSON_Delete(json);
    return card_array;
}

Card read_card(const char* data)
{
    cJSON* json = cJSON_Parse(data);
    cJSON* id = cJSON_GetObjectItem(json, "id");
    cJSON* title = cJSON_GetObjectItem(json, "title");
    cJSON* properties = cJSON_GetObjectItem(json, "properties");
    cJSON* sprint = cJSON_GetObjectItem(properties, "id_12");

    Card card = {
        .id = id->valueint,
        .sprint = (sprint == NULL) ? 0 : sprint->valueint,
        .title = create_string(title->valuestring)
    };
    cJSON_Delete(json);
    return card;
}

void delete_card_array(Card_array* card_array)
{
    for (int i = 0; i < card_array->size; ++i) {
        delete_string(&card_array->card_ptr[i].title);
    }
    free(card_array->card_ptr);
}

void deallocate_card(Card* card)
{
    delete_string(&card->title);
    free(card);
}

Card* allocate_card_from_copy(const Card* card)
{
    Card* result = (Card*)malloc(sizeof(Card));
    result->id = card->id;
    result->type = card->type;
    result->sprint = card->sprint;
    result->title = create_string(card->title.ptr);
    return result;
}
