#include "kaiten_endpoint.h"
#include "string.h"
#include <stdio.h>
#include <stdlib.h>

String kaiten_current_user_url(const Env* env)
{
    return add_string_const_char(&env->kaiten_host, "/api/latest/users/current");
}

/// [HOST]/api/latest/cards
String kaiten_cards_url(const Env* env)
{
    return add_string_const_char(&env->kaiten_host, "/api/latest/cards");
}

String kaiten_card_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    static const char* format = "/%u";

    int length = snprintf(NULL, 0,
        format,
        id);

    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1, format, id);
    return url;
}

String kaiten_card_children_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    static const char* format = "/%u/children";

    int length = snprintf(NULL, 0,
        format,
        id);

    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1, format, id);
    return url;
}

String kaiten_members_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    static const char* format = "/%u/members";

    int length = snprintf(NULL, 0,
        format,
        id);

    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1, format, id);
    return url;
}

String kaiten_member_url(const Env* env, int id, int user_id)
{
    String url = kaiten_cards_url(env);
    static const char* format = "/%u/members/%u";

    int length = snprintf(NULL, 0,
        format,
        id, user_id);

    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1,
        format,
        id, user_id);
    return url;
}

String kaiten_card_tags_url(const Env* env, int id)
{
    String url = kaiten_cards_url(env);
    static const char* format = "/%u/tags";

    int length = snprintf(NULL, 0,
        format,
        id);

    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1, format, id);
    return url;
}
