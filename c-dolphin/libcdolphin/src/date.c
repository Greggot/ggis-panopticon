#include "date.h"
#include <stdio.h>

#define TO_INT_NEXT(char_ptr) (*(char_ptr++) - 0x30)

Date date_from_string(const char* data)
{
    Date date = {
        .day = 0,
        .month = 0,
        .year = 0,
    };

    for (int i = 0; i < 8; ++i) {
        if (data[i] == 0) {
            printf("Incorrect date format: too short for YYYY-M-D\n");
            return date;
        }
    }

    const char* ptr = data;
    date.year += 1000 * TO_INT_NEXT(ptr);
    date.year += 100 * TO_INT_NEXT(ptr);
    date.year += 10 * TO_INT_NEXT(ptr);
    date.year += TO_INT_NEXT(ptr);
    ++ptr;

    if (*(ptr + 1) != '-')
        date.month += 10 * TO_INT_NEXT(ptr);
    date.month += TO_INT_NEXT(ptr);
    ++ptr;

    if (*(ptr + 1) != 0)
        date.day += 10 * TO_INT_NEXT(ptr);
    date.day += *ptr - '0';
    return date;
}

void date_to_string(char buffer[10], const Date* date)
{
    char* ptr = buffer;
    int year = date->year;

    ptr = &buffer[3];
    for (int i = 0; i < 4; ++i, --ptr) {
        *ptr = (year % 10) + '0';
        year /= 10;
    }

    ptr = &buffer[4];
    *(ptr++) = '-';
    *(ptr++) = date->month < 10 ? '0' : '1';
    *(ptr++) = (date->month % 10) + '0';
    *(ptr++) = '-';

    ++ptr;
    int day = date->day;
    *(ptr--) = (day % 10) + '0';
    day /= 10;
    *ptr = (day % 10) + '0';
}

int weekday(int day, int month, int year)
{
    if (month < 3) {
        month += 12;
        year--;
    }
    int J = year / 100;
    int K = year % 100;
    int h = (day + (13 * ++month) / 5 + K + K / 4 + J / 4 - 2 * J) % 7;
    h = (h + 7) % 7;
    return h;
}

const char* month_name(int month)
{
    static const char* month_names[] = {
        "Декабрь",
        "Январь",
        "Ферваль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
    };
    return month_names[month % 12];
}

int is_leap_year(int year)
{
    return (year % 4 == 0 && year % 100 != 0) || (year % 400 == 0);
}

int days_in_month(int month, int year)
{
    month %= 12;
    static const int days[] = { 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30 };
    if (month == 2 && is_leap_year(year))
        return 29;
    return days[month];
}

void next_day(int* day, int* month, int* year)
{
    ++(*day);
    if (*day <= days_in_month(*month, *year))
        return;

    *day = 1;
    ++(*month);
    if (*month < 12)
        return;

    *month = 1;
    ++(*year);
}

int is_day_off(const Date* date)
{
    return weekday(date->day, date->month, date->year) < 2;
}

int is_day_off_string(const char* date_str)
{
    Date date = date_from_string(date_str);
    return weekday(date.day, date.month, date.year) < 2;
}

void date_tests(void)
{
    char date_str[10] = "2025-03-00";
    Date date = date_from_string(date_str);
    // for (int i = 1; i < 32; ++i) {
    //     date.day = i;
    // }

    // date.month = 4;
    // for (int i = 1; i < 31; ++i) {
    //     date.day = i;
    //     is_day_off(&date);
    // }

    date.day = 30;
    date.month = 12;
    date.year = 2023;

    for (int i = 0; i < 66; ++i) {
        next_day(&date.day, &date.month, &date.year);
        printf("%u-%u-%u\n", date.day, date.month, date.year);
        date_to_string(date_str, &date);
        printf("%s\n\n", date_str);
    }

    // is_day_off_string("2025-03-1");
    // is_day_off_string("2025-3-2");
    // is_day_off_string("2025-03-03");
    // is_day_off_string("2025-03-4");
    // is_day_off_string("2025-3-05");
    // is_day_off_string("2025-3-6");
    // is_day_off_string("2025-3-7");
    // is_day_off_string("2025-3-8");
    // is_day_off_string("2025-3-9");
    // is_day_off_string("2025-3-10");
}
