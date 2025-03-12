#include "kaiten_endpoint.h"

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
