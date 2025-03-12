#include "card.h"
#include "card_creation.h"
#include "dev_tasks.h"
#include "env.h"
#include "kaiten_endpoint.h"
#include "requests.h"
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

void skird(const Env* env, const User* user, const Dev_task_list* dev, Create_paramters* parameters)
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

        parameters->parent = NULL;

        printf("[] USER_STORY\n");
        parent_request.type_id = USER_STORY;
        parameters->parent = request_current_card(env, &parent_request);

        if (parameters->parent == NULL) {
            printf("[] ENABLER\n");
            parent_request.type_id = ENABLER;
            parameters->parent = request_current_card(env, &parent_request);
        }

        if (parameters->parent == NULL) {
            printf("[] BUG\n");
            parent_request.type_id = BUG;
            parameters->parent = request_current_card(env, &parent_request);
        }

        if (parameters->parent == NULL) {
            printf("[] TECHDEBT\n");
            parent_request.type_id = TECHDEBT;
            parameters->parent = request_current_card(env, &parent_request);
        }

        if (parameters->parent == NULL)
            printf("[X] Search finished\n");

        Task_list* task_ptr = story_ptr->story.tasks_head;
        while (task_ptr != NULL) {
            parameters->title = task_ptr->task;
            create_card(env, user, parameters);
            task_ptr = task_ptr->next;
        }

        if (parameters->parent == NULL)
            printf("[ ] Search FAILED\n");
        else
            deallocate_card(parameters->parent);
        printf("\n");
        story_ptr = story_ptr->next;
    }
}

/// @brief По моит эмпирическим догадкам все виды карточек содержат
/// бред в начале, после которого ставится @b точка, после которой
/// идет месиво из цифр-букв, других точек до тех пор, пока не появится
/// @b пробел. Не знаю, почему пробел, но я нашел его во всех карточках,
/// которые мне было не лень просмотреть (где-то штук 20)
String_view ggis_id_from_title(String_view title)
{
    String_view string_view = {
        .ptr = title.ptr,
        .size = 0
    };

    while (*string_view.ptr != '.')
        ++string_view.ptr;
    ++string_view.ptr;
    const char* ptr = string_view.ptr;
    while (*ptr != ' ' && *ptr != 0) {
        ++ptr;
        ++string_view.size;
    }
    if (*ptr != 0)
        --string_view.size;
    return string_view;
}

#if GGIS_ID_TEST
#include <ctype.h>
void test_ggis_id_case(const char* text)
{
    String_view input = create_string_view(text);
    String_view result = ggis_id_from_title(input);

    printf("[");
    print_string_view(&result);
    printf("]\n");
}

void test_ggis_id(void)
{
    test_ggis_id_case("[CAD]:EN.98.1. Проработать концепцию работы инструмента");
    test_ggis_id_case("[CAD]:BUG.110.44746. Не выполняется операция");
    test_ggis_id_case("[CAD]:TS.76.36867.36935. Нет объема у некоторых ПМ после импорта на ");
    test_ggis_id_case("[CAD]:BUG.56e.22.45353. СЦЕНАРИЙ 5.3. Отсут");
    test_ggis_id_case("[CAD]:EN.40e.1. Созданий копий исходных полигона");
    test_ggis_id_case("[CAD]:F.113. Модель поиска");
    test_ggis_id_case("[CAD]:DB.x.45908. Есть возможность экспортировать в");
    test_ggis_id_case("[CAD]:DB.x.4590");
    test_ggis_id_case("DB..4590");
    test_ggis_id_case("[CAD]:TS.E.47-4.41617. Отрефакторить получение данных");
    test_ggis_id_case("[MGM]:TS.1.4.44460. fe-common-audit. Добавить поле Количество записей в выгрузке csv");
}
#endif

int main(void)
{
#if GGIS_ID_TEST
    test_ggis_id();
#endif

    Env env = read_env("../env/env.json");
    Dev_task_list dev = parse_task_list("data.txt");
    Skird_config skird_config = read_skird_config("../env/skird_config/delivery.json");

    requests_init();
    User user = request_current_user(&env);

    String_view tags[2] = { create_string_view("ГГИС"), create_string_view("C++") };
    Create_paramters create_parameters = {
        .title = create_string_view("Created by C"),
        .parent = NULL,
        .config = &skird_config,
        .tags_ptr = tags,
        .tags_size = sizeof(tags) / sizeof(String)
    };
    skird(&env, &user, &dev, &create_parameters);

    requests_deinit();
    clean_task_list(&dev);
    delete_skird_config(&skird_config);
    delete_env(&env);
    delete_user(&user);
}
