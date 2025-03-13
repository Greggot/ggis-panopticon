#include "card.h"
#include "card_creation.h"
#include "dev_tasks.h"
#include "env.h"
#include "ggis.h"
#include "kaiten_endpoint.h"
#include "requests.h"
#include "skird_config.h"
#include "string.h"
#include "string_view.h"
#include "user.h"
#include <ctype.h>
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
            printf("    [%u](%u) %s\n", result->id, result->sprint, result->title.ptr);
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

        if (parameters->parent != NULL) {
            printf("[X] Search finished, found with id {");
            String_view parent_title_view = create_string_view(parameters->parent->title.ptr);
            parameters->ggis_id = ggis_id_from_title(&parent_title_view);
            print_string_view(&parameters->ggis_id);
            printf("}\n");
        } else {
            parameters->ggis_id = story_ptr->story.parent_story;
        }

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

int does_user_agree(void)
{
    printf("Согласен? Y/N\n");
    char answer = toupper(getchar());
    return answer == 'Y';
}

int main(void)
{
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
    if (!does_user_agree())
        return 0;
    skird(&env, &user, &dev, &create_parameters);

    requests_deinit();
    clean_task_list(&dev);
    delete_skird_config(&skird_config);
    delete_user(&user);
    delete_env(&env);
}
