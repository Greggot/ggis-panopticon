#include "card.h"
#include "dev_tasks.h"
#include "env.h"
#include "kaiten_endpoint.h"
#include "skird_config.h"
#include "string.h"
#include "string_view.h"
#include "user.h"
#include <cjson/cJSON.h>
#include <curl/curl.h>
#include <curl/easy.h>

typedef enum {
    ARCHIVED,
    ACTIVE
} Card_condition;

static CURL* curl;

size_t get_callback(void* contents, size_t size, size_t nmemb, void* string_ptr)
{
    static long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code != 200) {
        printf("Error responce code: [%li]%s\n", response_code, (char*)contents);
        return size * nmemb;
    }

    String* string = (String*)string_ptr;
    if (string == NULL) {
        printf("Incorrect passed parameter\n");
        return size * nmemb;
    }

    String_view chunk = {
        .ptr = (char*)contents,
        .size = nmemb
    };
    add_string_to_string_view(string, &chunk);
    return size * nmemb;
}

void request_current_user(const Env* env)
{
    String kaiten_user_url = kaiten_current_user_url(env);
    String kaiten_auth = kaiten_auth_header(env);
    String overall_json = { .ptr = NULL, .size = 0 };

    curl_easy_setopt(curl, CURLOPT_URL, kaiten_user_url.ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, get_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);

    User user = read_user(overall_json.ptr);
    printf("USER: [%u] %s\n", user.id, user.full_name.ptr);

    delete_user(&user);
    delete_string(&overall_json);
    delete_string(&kaiten_user_url);
    delete_string(&kaiten_auth);
}

void request_current_card(const Env* env, const Card_request* request)
{
    String kaiten_get_card_url = card_get_request(env, request);
    String kaiten_auth = kaiten_auth_header(env);
    String overall_json = { .ptr = NULL, .size = 0 };
    curl_easy_setopt(curl, CURLOPT_URL, kaiten_get_card_url.ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, get_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);

    Card_array card_array = read_cards(overall_json.ptr);
    for (int i = 0; i < card_array.size; ++i) {
        printf("  [%u] %s\n", card_array.card_ptr[i].id, card_array.card_ptr[i].title.ptr);
    }
    delete_card_array(&card_array);

    delete_string(&kaiten_get_card_url);
    delete_string(&overall_json);
    delete_string(&kaiten_auth);
}

int main(void)
{
    Dev_task_list dev = parse_task_list("data.txt");
    clean_task_list(&dev);

    Env env = read_env("../env/env.json");
    printf("Accessing host: %s\n", env.kaiten_host.ptr);

    Skird_config skird_config = read_skird_config("../env/skird_config/delivery.json");
    printf("Config: %s\n", skird_config.size_text.ptr);

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if (curl == NULL) {
        return -1;
    }

    request_current_user(&env);

    Card_request request = {
        .type_id = ENABLER,
        .condition = ACTIVE,
        .offset = 0,
        .limit = 100,
        .query = create_string_view("EN.131.14")
    };
    request_current_card(&env, &request);

    curl_easy_cleanup(curl);
    curl_global_cleanup();
    delete_skird_config(&skird_config);
    delete_env(&env);
}
