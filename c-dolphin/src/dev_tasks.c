#include "dev_tasks.h"
#include "string_view.h"
#include <ctype.h>
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
    printf("Story \"");
    print_string_view(&story->parent_story);
    printf("\"\n");

    Task_list* list = story->tasks_head;
    while (list != NULL) {
        printf("\t");
        print_string_view(&list->task);
        printf("\n");
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

const char* type_to_string(String_type type)
{
    static const char* strings[4] = { "none", "parent", "task", "author" };
    return strings[(int)type];
}

void print_with_type(const String_view* string_view)
{
    printf("[%s] ", type_to_string(string_type(string_view)));
    print_string_view(string_view);
    printf("\n");
}

void read_file(Dev_task_list* dev, size_t* size, const char* path)
{
    FILE* file = fopen(path, "rb");
    if (file == NULL) {
        printf("Cannot read file \"%s\"", path);
        return;
    }

    fseek(file, 0, SEEK_END);
    *size = ftell(file);
    fseek(file, 0, SEEK_SET);

    dev->file_data = (char*)malloc(*size);
    if (dev->file_data == NULL) {
        printf("Cannot allocate text_data");
        return;
    }

    fread(dev->file_data, 1, *size, file);
    fclose(file);
}

int char_is_correct(char c)
{
    return c != '\n' || c != 0;
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
    free(dev->file_data);
}

Dev_task_list parse_task_list(const char* path)
{
    Dev_task_list dev;
    dev.head_story = NULL;
    dev.file_data = NULL;

    size_t size = 0;
    read_file(&dev, &size, path);

    Story story;
    story.tasks_head = NULL;

    char* begin_ptr = dev.file_data;
    char* end_ptr = dev.file_data;

    for (size_t i = 0; i < size;)
    {
        while (i < size && char_is_correct(*end_ptr)) {
            ++end_ptr;
            ++i;
        }

        String_view string_view = {
            .ptr = begin_ptr,
            .size = end_ptr - begin_ptr - 1
        };
        begin_ptr = ++end_ptr;

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
