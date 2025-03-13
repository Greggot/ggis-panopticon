cmake_minimum_required(VERSION 3.5)
project(panopticon_c C)

# TODO: добавить отдельную библиотеку для time_log, 
# ему нужно куда меньше ресурсов
add_subdirectory(libcdolphin)
add_executable(skird main_skird.c)
add_executable(time_log main_time_log.c)

target_compile_options(skird PRIVATE 
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
target_compile_options(time_log PRIVATE 
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

target_include_directories(skird PUBLIC "libcdolphin/src")
target_include_directories(time_log PUBLIC "libcdolphin/src")

target_link_libraries(skird PUBLIC libcdolphin)
target_link_libraries(time_log PUBLIC libcdolphin)
