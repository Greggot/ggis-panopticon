#include "card.h"
#include "kaiten_endpoint.h"
#include "string.h"
#include <stdio.h>
#include <stdlib.h>

String card_get_request(const Env* env, const Card_request* request)
{
    static const char* format = "?type_id=%i&condition=%i&offset=%i&limit=%i&query=%.*s";
    int length = snprintf(NULL, 0,
        format,
        request->type_id, request->condition, request->offset,
        request->limit, (int)request->query.size, request->query.ptr);

    String url = kaiten_card_url(env);
    const size_t prev_size = url.size;
    url.size += length;
    url.ptr = realloc(url.ptr, url.size);
    snprintf(url.ptr + prev_size, length, format,
        request->type_id, request->condition, request->offset,
        request->limit, (int)request->query.size, request->query.ptr);
    return url;
}
