#pragma once
#include "cd_string.h"
#include "string_view.h"

typedef struct Task_list_t {
    String_view task;
    struct Task_list_t* next;
} Task_list;

/// @brief Связь родительской стори с дочерними карточками
typedef struct {
    String_view parent_story;
    Task_list* tasks_head;
    Task_list* current_task;
} Story;

typedef struct Story_list_t {
    Story story;
    struct Story_list_t* next;
} Story_list;

typedef struct {
    Story_list* head_story;
    Story_list* current_story;
    String file_data;
} Dev_task_list;

Dev_task_list parse_task_list(const char*);
void clean_task_list(Dev_task_list*);
