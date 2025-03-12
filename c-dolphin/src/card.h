#pragma once

#include "env.h"
#include "string.h"
#include "string_view.h"

typedef enum {
    USER_STORY = 5,
    BUG = 7,
    ENABLER = 8,
    TECHDEBT = 9,
} Card_type;

typedef struct {
    unsigned int id;
    unsigned int sprint;
    String title;
    Card_type type;
} Card;

typedef struct {
    Card* card_ptr;
    int size;
} Card_array;

typedef struct {
    int type_id;
    int condition;
    int offset;
    int limit;
    String_view query;
} Card_request;

String card_get_request(const Env*, const Card_request*);
Card_array read_cards(const char*);
Card read_card(const char*);

void delete_card_array(Card_array*);
void deallocate_card(Card*);
Card* allocate_card_from_copy(const Card*);
