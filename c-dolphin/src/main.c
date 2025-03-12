#include "card.h"
#include "card_creation.h"
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
#include <stdio.h>
#include <stdlib.h>

typedef enum {
    ARCHIVED,
    ACTIVE
} Card_condition;

static CURL* curl;

/// @brief Собирает все части ответа сервера в одну строку по string_ptr
size_t get_callback(void* contents, size_t size, size_t nmemb, void* string_ptr)
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

/// @return JSON-ответ на GET-запрос по url
/// @param env хранит токен аутентификации
String request_get(const Env* env, const String* url)
{
    String kaiten_auth = kaiten_auth_header(env);
    String overall_json = { .ptr = NULL, .size = 0 };

    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, get_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);

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

User request_current_user(const Env* env)
{
    String kaiten_user_url = kaiten_current_user_url(env);
    String answer = request_get(env, &kaiten_user_url);
    User user = read_user(answer.ptr);

    printf("USER: [%u] %s\n", user.id, user.full_name.ptr);

    delete_string(&answer);
    delete_string(&kaiten_user_url);
    return user;
}

/// @todo Заменить Card* на стркутуру, в которой будет описан статус
/// В теории можно было возвращать Card_array, если под имя стори подходит
/// несолько различных карточек
Card* request_current_card(const Env* env, const Card_request* request)
{
    String kaiten_card_url = card_get_request(env, request);
    String answer = request_get(env, &kaiten_card_url);
    Card_array card_array = read_cards(answer.ptr);

    Card* result = NULL;
    int found = 0;

    printf("%s\n", answer.ptr);

    for (int i = 0; i < card_array.size && !found; ++i) {
        Card* card = &card_array.card_ptr[i];
        found = string_contains_substring_view(&card->title, &request->query);
        if (found) {
            result = allocate_card_from_copy(card);
            printf("    [%u] %s\n", result->id, result->title.ptr);
        }
    }

    delete_card_array(&card_array);
    delete_string(&answer);
    delete_string(&kaiten_card_url);

    return result;
}

void skird(const Env* env, const Dev_task_list* dev)
{
    Story_list* story_ptr = dev->head_story;
    Card_request parent_request = {
        .condition = ACTIVE,
        .offset = 0,
        .limit = 100,
    };

    while (story_ptr != NULL) {
        parent_request.query = story_ptr->story.parent_story;
        printf("[] Search (%zu) ", story_ptr->story.parent_story.size);
        print_string_view(&story_ptr->story.parent_story);
        printf("...\n");

        Card* parent_card = NULL;

        printf("[] USER_STORY\n");
        parent_request.type_id = USER_STORY;
        parent_card = request_current_card(env, &parent_request);

        if (parent_card == NULL) {
            printf("[] ENABLER\n");
            parent_request.type_id = ENABLER;
            parent_card = request_current_card(env, &parent_request);
        }

        if (parent_card == NULL) {
            printf("[] BUG\n");
            parent_request.type_id = BUG;
            parent_card = request_current_card(env, &parent_request);
        }

        if (parent_card == NULL) {
            printf("[] TECHDEBT\n");
            parent_request.type_id = TECHDEBT;
            parent_card = request_current_card(env, &parent_request);
        }

        if (parent_card == NULL)
            printf("[ ] Search FAILED\n\n");
        else {
            printf("[X] Search finished\n\n");
            deallocate_card(parent_card);
        }
        story_ptr = story_ptr->next;
    }
}

int main(void)
{
    Env env = read_env("../env/env.json");
    printf("Accessing host: %s\n", env.kaiten_host.ptr);

    Skird_config skird_config = read_skird_config("../env/skird_config/delivery.json");
    printf("Config: %s\n", skird_config.size_text.ptr);

    Dev_task_list dev = parse_task_list("data.txt");

    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();

    String tags[2] = { create_string("ГГИС"), create_string("C++") };

    User user = request_current_user(&env);
    Card parent_card = {
        .id = 46276,
        .sprint = 53,
        .title = create_string("[CAD]:EN.131.13. Реализовать работу с компонентами связанности меша")
    };
    Create_paramters create_parameters = {
        .title = create_string_view("Created by C"),
        .parent = &parent_card,
        .config = &skird_config,
        .tags_ptr = tags,
        .tags_size = sizeof(tags) / sizeof(String)
    };
    create_card(curl, &env, &user, &create_parameters);
    // skird(&env, &dev);

    curl_easy_cleanup(curl);
    curl_global_cleanup();
    clean_task_list(&dev);
    delete_skird_config(&skird_config);
    delete_env(&env);
    delete_user(&user);

    for (size_t i = 0; i < create_parameters.tags_size; ++i) {
        delete_string(&tags[i]);
    }
}
