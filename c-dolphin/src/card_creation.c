#include "card_creation.h"
#include "card.h"
#include "kaiten_endpoint.h"
#include "string.h"
#include <cjson/cJSON.h>
#include <curl/curl.h>
#include <stdlib.h>
#include <string.h>

CURL* curl;

/// @brief Собирает все части ответа сервера в одну строку по string_ptr
size_t post_callback(void* contents, size_t size, size_t nmemb, void* string_ptr)
{
    static long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code != 200) {
        printf("Error responce code: [%li]%s\n", response_code, (char*)contents);
        return size * nmemb;
    }

    String* string = (String*)string_ptr;
    String_view chunk = {
        .ptr = (char*)contents,
        .size = nmemb
    };
    add_string_to_string_view(string, &chunk);
    return size * nmemb;
}

String request_post(const Env* env, const String* url, const String* data)
{
    String kaiten_auth = kaiten_auth_header(env);
    String overall_json = { .ptr = NULL, .size = 0 };

    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, post_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);

    delete_string(&kaiten_auth);
    return overall_json;
}

String post_card_create_data(const Create_paramters* creator, const User* user)
{
    cJSON* root = cJSON_CreateObject();

    cJSON_AddStringToObject(root, "title", creator->title.ptr);
    cJSON_AddNumberToObject(root, "board_id", creator->config->board_id);
    cJSON_AddNumberToObject(root, "column_id", creator->config->column_id);
    cJSON_AddNumberToObject(root, "lane_id", creator->config->lane_id);
    cJSON_AddStringToObject(root, "size_text", creator->config->size_text.ptr);
    cJSON_AddNumberToObject(root, "type_id", creator->config->type_id);
    cJSON_AddNumberToObject(root, "owner_id", user->id);
    cJSON_AddStringToObject(root, "owner_email", user->email.ptr);

    cJSON* properties = cJSON_CreateObject();
    cJSON_AddStringToObject(properties, "id_19", creator->config->magic_properties.id_19.ptr);
    cJSON_AddItemToObject(root, "properties", properties);

    String json;
    json.ptr = cJSON_Print(root);
    json.size = strlen(json.ptr);

    cJSON_Delete(root);
    return json;
}

static void post_card_add_tag(const Env* env, const String* tag, int id)
{
    cJSON* root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, "name", tag->ptr);
    String json;
    json.ptr = cJSON_Print(root);

    String tags_url = kaiten_card_tags_url(env, id);
    String answer = request_post(env, &tags_url, &json);
    printf("Tags endpoint: %s\n", tags_url.ptr);

    delete_string(&tags_url);
    delete_string(&answer);
    delete_string(&json);
}

void create_card(CURL* in_curl, const Env* env, const User* user, const Create_paramters* creator)
{
    curl = in_curl;
    String url = kaiten_card_url(env);
    String post_data = post_card_create_data(creator, user);
    String answer = request_post(env, &url, &post_data);
    Card created_card = read_card(answer.ptr);

    printf("POST data: \n%s\n", post_data.ptr);
    printf("POST answer: %s\n", answer.ptr);
    for (size_t i = 0; i < creator->tags_size; ++i) {
        post_card_add_tag(env, &creator->tags_ptr[i], created_card.id);
    }

    delete_string(&created_card.title);
    delete_string(&answer);
    delete_string(&post_data);
    delete_string(&url);
}
