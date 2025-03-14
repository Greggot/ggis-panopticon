#pragma once

typedef struct {
    int day;
    int month;
    int year;
} Date;

Date date_from_string(const char* data);
/// @brief Заполняет buffer строкой даты формата YYYY-MM-DD
void date_to_string(char buffer[10], const Date* date);

/// @brief Zeller's congruence - формула для вычисления дня недели из 19 века
int weekday(int day, int month, int year);

const char* month_name(int month);

int is_leap_year(int year);

int days_in_month(int month, int year);

void next_day(int* day, int* month, int* year);

/// @todo Подключить API какое-нибудь для праздников и всего такого
int is_day_off(const Date* date);
int is_day_off_string(const char* date_str);

void date_tests(void);
