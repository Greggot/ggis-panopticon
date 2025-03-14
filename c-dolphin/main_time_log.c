#include "auto_time_log.h"
#include "env.h"
#include "requests.h"
#include <ctype.h>
#include <stdio.h>

int does_user_agree(void)
{
    printf("Согласен? Y/N\n");
    char answer = toupper(getchar());
    return answer == 'Y';
}

int main(void)
{
    Env env = read_env("../env/env.json");
    requests_init();

    Time_log_config time_log_config = read_time_log_config("../env/auto_time_log.json");

    what_write_time_log_gonna_do(&env, &time_log_config);
    if (does_user_agree())
        write_time_log(&env, &time_log_config);

    requests_deinit();
    delete_env(&env);
}
