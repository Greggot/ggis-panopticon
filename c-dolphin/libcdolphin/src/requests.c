#include "requests.h"
#include <curl/curl.h>

CURL* curl;

size_t collect_string_callback(void* contents, size_t size, size_t nmemb, void* string_ptr);
size_t status_callback(void* contents, size_t size, size_t nmemb, void* unused);

String request_get(const Env* env, const String* url)
{
    String overall_json = { .ptr = NULL, .size = 0 };

    curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "GET");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, collect_string_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    return overall_json;
}

String request_post(const Env* env, const String* url, const String* data)
{
    String overall_json = { .ptr = NULL, .size = 0 };

    curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, collect_string_callback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &overall_json);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);

    return overall_json;
}

void request_post_no_answer(const Env* env, const String* url, const String* data)
{
    curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_POST, 1L);
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "POST");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, status_callback);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
}

void request_patch(const Env* env, const String* url, const String* data)
{
    curl = curl_easy_init();
    curl_easy_setopt(curl, CURLOPT_URL, url->ptr);
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, status_callback);
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, data->ptr);
    curl_easy_setopt(curl, CURLOPT_CUSTOMREQUEST, "PATCH");

    struct curl_slist* headers = NULL;
    headers = curl_slist_append(headers, "Accept: application/json");
    headers = curl_slist_append(headers, "Content-Type: application/json");
    headers = curl_slist_append(headers, env->kaiten_auth.ptr);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);
    curl_easy_perform(curl);
    curl_slist_free_all(headers);
    curl_easy_cleanup(curl);
}

/// ------------------------------ CALLBACKS ------------------------------ ///  

size_t collect_string_callback(void* contents, size_t size, size_t nmemb, void* string_ptr)
{
    static long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code != 200) {
        printf("Error responce code: [%li]%s\n", response_code, (char*)contents);
        return size * nmemb;
    }

    // printf("%s", (char*)contents);

    String* string = (String*)string_ptr;
    String_view chunk = {
        .ptr = (char*)contents,
        .size = nmemb
    };
    add_string_to_string_view(string, &chunk);
    return size * nmemb;
}

size_t status_callback(void* contents, size_t size, size_t nmemb, void* unused)
{
    (void)unused;
    static long response_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &response_code);
    if (response_code != 200) {
        printf("Error responce code: [%li] %s\n", response_code, (char*)contents);
    }
    return size * nmemb;
}
void requests_init(void) 
{ 
    curl_global_init(CURL_GLOBAL_DEFAULT);
}

void requests_deinit(void)
{
    curl_global_cleanup();
}
