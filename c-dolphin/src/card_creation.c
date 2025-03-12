#include "card_creation.h"
#include "card.h"
#include "kaiten_endpoint.h"
#include "string.h"
#include "string_view.h"
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

size_t status_callback(void* contents, size_t size, size_t nmemb, void* unused)
{
    (void)unused;
    static long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code != 200) {
        printf("Error responce code: [%li] %s\n", response_code, (char*)contents);
    }
    return size * nmemb;
}

String request_post(const Env* env, const String* url, const String* data)
{
    String overall_json = { .ptr = NULL, .size = 0 };

    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, post_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);

    return overall_json;
}

void request_post_no_answer(const Env* env, const String* url, const String* data)
{
    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, status_callback);
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);
}

void request_patch(const Env* env, const String* url, const String* data)
{
    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, status_callback);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PATCH");

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);
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
    if (creator->parent && creator->parent->sprint)
        cJSON_AddNumberToObject(properties, "id_12", creator->parent->sprint);
    cJSON_AddItemToObject(root, "properties", properties);

    String json;
    json.ptr = cJSON_Print(root);
    json.size = strlen(json.ptr);

    cJSON_Delete(root);
    return json;
}

/// @todo GGIS ID from parent card
String ggis_card_title(const Card* card)
{
    static const char* format = "[CAD]:TS.%s.%u. %s";
    int length = snprintf(NULL, 0,
        format,
        "131.13", card->id, card->title.ptr);

    String new_title;
    new_title.size += length + 1;
    new_title.ptr = (char*)malloc(new_title.size);

    snprintf(new_title.ptr, length + 1, format,
        "131.13", card->id, card->title.ptr);
    return new_title;
}

static String json_single_string(const char* key, const String* value)
{
    cJSON* root = cJSON_CreateObject();
    cJSON_AddStringToObject(root, key, value->ptr);
    String json;
    json.ptr = cJSON_Print(root);
    cJSON_Delete(root);
    return json;
}

static String json_single_int(const char* key, int value)
{
    cJSON* root = cJSON_CreateObject();
    cJSON_AddNumberToObject(root, key, value);
    String json;
    json.ptr = cJSON_Print(root);
    cJSON_Delete(root);
    return json;
}

static void post_card_add_tag(const Env* env, const String* tag, int id)
{
    String json = json_single_string("name", tag);
    String tags_url = kaiten_card_tags_url(env, id);
    request_post_no_answer(env, &tags_url, &json);

    delete_string(&tags_url);
    delete_string(&json);
}

static void patch_card_title(const Env* env, const Card* card)
{
    String card_url = kaiten_card_url(env, card->id);
    String new_title = ggis_card_title(card);
    String json = json_single_string("title", &new_title);
    request_patch(env, &card_url, &json);

    delete_string(&new_title);
    delete_string(&card_url);
    delete_string(&json);
}

static void post_card_add_user(const Env* env, const Card* card, const User* user)
{
    {
        String members_url = kaiten_members_url(env, card->id);
        String json = json_single_int("user_id", user->id);
        request_post_no_answer(env, &members_url, &json);

        delete_string(&json);
        delete_string(&members_url);
    }
    {
        String members_url = kaiten_member_url(env, card->id, user->id);
        String json = json_single_int("type", OWNER);
        request_patch(env, &members_url, &json);

        delete_string(&json);
        delete_string(&members_url);
    }
}

static void post_card_add_child(const Env* env, const Card* parent, const Card* child)
{
    String children_url = kaiten_card_children_url(env, parent->id);
    String json = json_single_int("card_id", child->id);
    request_post_no_answer(env, &children_url, &json);

    delete_string(&json);
    delete_string(&children_url);
}

void create_card(CURL* in_curl, const Env* env, const User* user, const Create_paramters* creator)
{
    curl = in_curl;
    String url = kaiten_cards_url(env);
    String post_data = post_card_create_data(creator, user);
    String answer = request_post(env, &url, &post_data);
    Card created_card = read_card(answer.ptr);

    if (creator->parent != NULL) {
        post_card_add_child(env, creator->parent, &created_card);
    }
    for (size_t i = 0; i < creator->tags_size; ++i) {
        post_card_add_tag(env, &creator->tags_ptr[i], created_card.id);
    }

    post_card_add_user(env, &created_card, user);
    patch_card_title(env, &created_card);
    printf("Created card: %s/%u\n", env->kaiten_host.ptr, created_card.id);

    delete_string(&post_data);
    delete_string(&answer);
    delete_string(&created_card.title);
    delete_string(&url);
}
