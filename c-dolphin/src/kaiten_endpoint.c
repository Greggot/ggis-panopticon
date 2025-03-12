#include "kaiten_endpoint.h"
#include <stdio.h>
#include <stdlib.h>

String kaiten_current_user_url(const Env* env)
{
    return add_string_const(&env->kaiten_host, "/api/latest/users/current");
}

String kaiten_auth_header(const Env* env)
{
    String left = create_string("Authorization: Bearer ");
    add_string_other(&left, &env->kaiten_token);
    return left;
}

String kaiten_card_url(const Env* env)
{
    return add_string_const(&env->kaiten_host, "/api/latest/cards");
}

String kaiten_card_tags_url(const Env* env, int id)
{
    String url = kaiten_card_url(env);
    static const char* format = "%s/%u/tags";

    int length = snprintf(NULL, 0,
        format,
        url.ptr, id);

    const size_t prev_size = url.size;
    url.size += length + 1;
    url.ptr = realloc(url.ptr, url.size);

    snprintf(url.ptr + prev_size, length + 1, format, url.ptr, id);
    return url;
}
