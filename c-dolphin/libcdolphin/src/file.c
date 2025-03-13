#include "file.h"
#include <stdio.h>
#include <stdlib.h>

String read_file_string(const char* path)
{ 
    String string = { .ptr = NULL, .size = 0 };
    FILE* file = fopen(path, "r");

    if (file == NULL) {
        printf("Cannot read file \"%s\"", path);
        return string;
    }

    fseek(file, 0, SEEK_END);
    string.size = ftell(file);
    fseek(file, 0, SEEK_SET);

    string.ptr = (char*)malloc(string.size + 1);
    if (string.ptr == NULL) {
        printf("Cannot allocate text_data");
        string.size = 0;
        return string;
    }

    fread(string.ptr, string.size, 1, file);
    fclose(file);

    string.ptr[string.size] = 0;
    ++string.size;
    return string;
}
