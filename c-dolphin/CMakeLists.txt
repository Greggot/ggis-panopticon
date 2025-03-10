cmake_minimum_required(VERSION 3.5)
project(panopticon_c C)

set(SOURCES 
    dev_tasks.c
    env.c
    main.c
    skird_config.c
    string_view.c
    string.c
    user.c
)
add_executable(panopticon_c ${SOURCES})

target_compile_options(panopticon_c PRIVATE 
    -Wall 
    -Wextra 
    -pedantic 
    -Wno-unused-macros 
    -Wno-unused-function 
    -Wno-unreachable-code 
    -Wno-padded 
    -Wno-reserved-identifier 
    -Wuninitialized
    # -fsanitize=address
)

find_package(CURL REQUIRED) 
find_package(cJSON REQUIRED)

message(STATUS "CJSON_LIBRARIES : ${CJSON_LIBRARIES}")
message(STATUS "CURL_LIBRARIES: ${CURL_LIBRARIES}")

target_link_libraries(panopticon_c PRIVATE ${CURL_LIBRARIES})
target_link_libraries(panopticon_c PRIVATE ${CJSON_LIBRARIES})