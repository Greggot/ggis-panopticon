#include "dev_tasks.h"
#include "env.h"
#include "skird_config.h"
#include "string.h"
#include "user.h"
#include <cjson/cJSON.h>
#include <curl/curl.h>
#include <curl/easy.h>

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

size_t write_callback(void* contents, size_t size, size_t nmemb, void* user_parameter)
{
    User user = read_user((char*)contents);
    printf("USER: [%u] %s\n", user.id, user.full_name.ptr);
    delete_user(&user);
    return size * nmemb;
}

int main(void)
{
    Dev_task_list dev = parse_task_list("../env/data.txt");
    clean_task_list(&dev);

    Env env = read_env("../env/env.json");
    printf("Accessing host: %.*s \n", (int)env.kaiten_host.size, env.kaiten_host.ptr);

    Skird_config skird_config = read_skird_config("../env/skird_config/delivery.json");
    printf("Config: %s\n", skird_config.size_text.ptr);
    delete_skird_config(&skird_config);

    CURL* curl;
    curl_global_init(CURL_GLOBAL_DEFAULT);
    curl = curl_easy_init();
    if (curl == NULL) {
        return -1;
    }

    char read_buffer[1024];
    String kaiten_user_url = kaiten_current_user_url(&env);
    String kaiten_auth = kaiten_auth_header(&env);
    curl_easy_setopt(curl, CURLOPT_URL, kaiten_user_url.ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, read_buffer);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    CURLcode result = curl_easy_perform(curl);
    if (result != CURLE_OK) {
        printf("cURL error: %s\n", curl_easy_strerror(result));
    } else {
        printf("%s\n", read_buffer);
    }

    curl_easy_cleanup(curl);
    curl_global_cleanup();
    delete_string(&kaiten_user_url);
    delete_string(&kaiten_auth);
}
