#include "kaiten_endpoint.h"
#include "string.h"
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>

/// [HOST]/api/latest/users/current
String kaiten_current_user_url(const Env* env)
{
    return add_string_const_char(&env->kaiten_host, "/api/latest/users/current");
}

/// [HOST]/api/latest/cards
String kaiten_cards_url(const Env* env)
{
    return add_string_const_char(&env->kaiten_host, "/api/latest/cards");
}

void append_formatted_string(String* url, const char* format, ...)
{
    va_list args;

    va_start(args, format);
    int length = vsnprintf(NULL, 0,
        format,
        args);
    va_end(args);

    const size_t prev_size = url->size;
    url->size += length + 1;
    url->ptr = realloc(url->ptr, url->size);

    va_start(args, format);
    vsnprintf(url->ptr + prev_size, length + 1,
        format,
        args);
    va_end(args);
}

/// [HOST]/api/latest/cards/{id}
String kaiten_card_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    append_formatted_string(&url, "/%u", id);
    return url;
}

/// [HOST]/api/latest/cards/{id}/children
String kaiten_card_children_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    append_formatted_string(&url, "/%u/children", id);
    return url;
}

/// [HOST]/api/latest/cards/{id}/members
String kaiten_members_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    append_formatted_string(&url, "/%u/members", id);
    return url;
}

/// [HOST]/api/latest/cards/{id}/members/{user_id}
String kaiten_member_url(const Env* env, int id, int user_id)
{
    String url = kaiten_cards_url(env);
    append_formatted_string(&url, "/%u/members/%u", id, user_id);
    return url;
}

/// [HOST]/api/latest/cards/{id}/tags
String kaiten_card_tags_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    append_formatted_string(&url, "/%u/tags", id);
    return url;
}

String kaiten_card_time_logs_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    append_formatted_string(&url, "/%i/time-logs", id);
    return url;
}
