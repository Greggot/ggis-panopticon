cmake_minimum_required(VERSION 3.5)
project(panopticon_c C)

FILE(GLOB SOURCES "src/*.c")
add_library(libcdolphin STATIC ${SOURCES})

target_compile_options(libcdolphin PRIVATE 
    -Wall 
    -Wextra 
    -pedantic 
    -Wno-unused-macros 
    -Wno-unused-function 
    -Wno-unreachable-code 
    -Wno-padded 
    -Wno-reserved-identifier 
    -Wuninitialized
)

find_package(CURL REQUIRED) 
find_package(cJSON REQUIRED)

target_link_libraries(libcdolphin PRIVATE ${CURL_LIBRARIES})
target_link_libraries(libcdolphin PRIVATE ${CJSON_LIBRARIES})
target_include_directories(libcdolphin PUBLIC "src")
target_compile_definitions(libcdolphin PRIVATE GGIS_ID_TEST=0)