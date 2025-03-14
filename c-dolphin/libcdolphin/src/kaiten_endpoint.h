
#include "env.h"
#include "cd_string.h"

String kaiten_current_user_url(const Env*);
String kaiten_cards_url(const Env*);
String kaiten_card_url(const Env*, int id);
String kaiten_card_children_url(const Env*, int id);
String kaiten_member_url(const Env*, int id, int user_id);
String kaiten_members_url(const Env*, int id);
String kaiten_card_tags_url(const Env*, int id);
String kaiten_card_time_logs_url(const Env*, int id);
