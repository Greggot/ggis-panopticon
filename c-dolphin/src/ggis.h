#pragma once

#include "string_view.h"

/// @brief По моит эмпирическим догадкам все виды карточек содержат
/// бред в начале, после которого ставится @b точка, после которой
/// идет месиво из цифр-букв, других точек до тех пор, пока не появится
/// @b пробел. Не знаю, почему пробел, но я нашел его во всех карточках,
/// которые мне было не лень просмотреть (где-то штук 20)
String_view ggis_id_from_title(const String_view*);

#if GGIS_ID_TEST
void test_ggis_id_case(const char* text);
void test_ggis_id(void);
#endif
