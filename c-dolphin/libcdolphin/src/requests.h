#pragma once

#include "cd_string.h"
#include "env.h"

void requests_init(void);
void requests_deinit(void);

String request_get(const Env*, const String* url);
String request_post(const Env*, const String* url, const String* data);
void request_post_no_answer(const Env*, const String* url, const String* data);
void request_patch(const Env*, const String* url, const String* data);
