#include "dev_tasks.h"
#include "file.h"
#include "string.h"
#include "string_view.h"
#include <stdio.h>
#include <stdlib.h>

typedef enum {
    NONE,
    PARENT,
    TASK,
    AUTHOR,
} String_type;

/// @brief Если строка пустая или состоит только из служебных
/// символов - у нее нет назначения
String_type string_type(const String_view* string_view)
{
    if (string_view->size == 0)
        return NONE;

    int is_empty = 1;
    for (size_t i = 0; i < string_view->size && is_empty; ++i)
        if (string_view->ptr[i] != ' ')
            is_empty = 0;
    if (is_empty)
        return NONE;

    const char id = string_view->ptr[0];
    if (id == ' ' || id == '\t')
        return TASK;
    if (id == '@')
        return AUTHOR;
    return PARENT;
}

Task_list* create_task(const String_view* task)
{
    Task_list* element = (Task_list*)malloc(sizeof(Task_list));
    element->task = *task;
    element->next = NULL;
    return element;
}

void add_task(Story* story, const String_view* task)
{
    if (story->tasks_head == NULL) {
        story->tasks_head = create_task(task);
        story->current_task = story->tasks_head;
    } else {
        story->current_task->next = create_task(task);
        story->current_task = story->current_task->next;
    }
}

void output_story(const Story* story)
{
    printf("Story \"%s\"\n", story->parent_story.ptr);

    Task_list* list = story->tasks_head;
    while (list != NULL) {
        printf("\t%s\n", list->task.ptr);
        list = list->next;
    }
}

Story_list* create_story(const Story* story)
{
    Story_list* element = (Story_list*)malloc(sizeof(Story_list));
    element->story = *story;
    element->next = NULL;
    return element;
}

void add_story(Dev_task_list* dev, const Story* story)
{
    if (dev->head_story == NULL) {
        dev->head_story = create_story(story);
        dev->current_story = dev->head_story;
    } else {
        dev->current_story->next = create_story(story);
        dev->current_story = dev->current_story->next;
    }
}

void output(const Dev_task_list* dev)
{
    Story_list* story = dev->head_story;
    while (story != NULL) {
        output_story(&story->story);
        story = story->next;
    }
}

/// -------------------------------- PUBLIC -------------------------------- ///

void clean_task_list(Dev_task_list* dev)
{
    Story_list* story = dev->head_story;
    while (story != NULL)
    {
        Task_list* task = story->story.tasks_head;
        while (task != NULL) {
            Task_list* prev = task;
            task = task->next;
            free(prev);
        }
        Story_list* prev = story;
        story = story->next;
        free(prev);
    }
    delete_string(&dev->file_data);
}

/// @todo Добавить автора - если встретилась такая строка, то
/// дописывать его ко всем последующим задачам, пока не встретится новый
Dev_task_list parse_task_list(const char* path)
{
    Dev_task_list dev;
    dev.head_story = NULL;
    dev.file_data = read_file_string(path);

    Story story;
    story.tasks_head = NULL;

    char* begin_ptr = dev.file_data.ptr;
    char* end_ptr = dev.file_data.ptr;

    for (size_t i = 0; i < dev.file_data.size && *end_ptr != 0;)
    {
        while (i < dev.file_data.size && *(end_ptr) != '\n' && *(end_ptr + 1) != 0) {
            ++end_ptr;
            ++i;
        }
        if (*end_ptr == '\n')
            *end_ptr = 0;

        String_view string_view = {
            .ptr = begin_ptr,
            .size = ++end_ptr - begin_ptr - 1
        };
        begin_ptr = end_ptr;

        switch (string_type(&string_view)) {
            case PARENT:
                if (story.tasks_head != NULL) {
                    add_story(&dev, &story);
                    story.tasks_head = NULL;
                }
                story.parent_story = string_view;
                break;

            case TASK:
                add_task(&story, &string_view);
                break;
            default:
                break;
        }
    }

    if (story.tasks_head != NULL) {
        add_story(&dev, &story);
    }
    output(&dev);
    return dev;
}
