#include "ggis.h"

String_view ggis_id_from_title(const String_view* title)
{
    String_view string_view = {
        .ptr = title->ptr,
        .size = 0
    };

    while (*string_view.ptr != '.')
        ++string_view.ptr;
    ++string_view.ptr;
    const char* ptr = string_view.ptr;
    while (*ptr != ' ' && *ptr != 0) {
        ++ptr;
        ++string_view.size;
    }
    if (*ptr != 0)
        --string_view.size;
    return string_view;
}

#if GGIS_ID_TEST
#include <stdio.h>
void test_ggis_id_case(const char* text)
{
    String_view input = create_string_view(text);
    String_view result = ggis_id_from_title(input);

    printf("[");
    print_string_view(&result);
    printf("]\n");
}

void test_ggis_id(void)
{
    test_ggis_id_case("[CAD]:EN.98.1. Проработать концепцию работы инструмента");
    test_ggis_id_case("[CAD]:BUG.110.44746. Не выполняется операция");
    test_ggis_id_case("[CAD]:TS.76.36867.36935. Нет объема у некоторых ПМ после импорта на ");
    test_ggis_id_case("[CAD]:BUG.56e.22.45353. СЦЕНАРИЙ 5.3. Отсут");
    test_ggis_id_case("[CAD]:EN.40e.1. Созданий копий исходных полигона");
    test_ggis_id_case("[CAD]:F.113. Модель поиска");
    test_ggis_id_case("[CAD]:DB.x.45908. Есть возможность экспортировать в");
    test_ggis_id_case("[CAD]:DB.x.4590");
    test_ggis_id_case("DB..4590");
    test_ggis_id_case("[CAD]:TS.E.47-4.41617. Отрефакторить получение данных");
    test_ggis_id_case("[MGM]:TS.1.4.44460. fe-common-audit. Добавить поле Количество записей в выгрузке csv");
}
#endif
