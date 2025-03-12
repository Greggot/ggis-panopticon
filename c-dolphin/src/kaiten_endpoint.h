
#include "env.h"
#include "string.h"

String kaiten_current_user_url(const Env*);
String kaiten_auth_header(const Env*);
String kaiten_card_url(const Env*);
String kaiten_card_tags_url(const Env* env, int id);
