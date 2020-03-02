cmake_minimum_required(VERSION 3.0)

project(fort VERSION 0.1.0)

set(CMAKE_VERBOSE_MAKEFILE ON)

# Embed libfort
set(FORT_ENABLE_TESTING OFF CACHE INTERNAL "")
add_subdirectory(libfort)

# Add main executable target.
add_executable(fort-app
    main.c)
set_target_properties(fort-app
    PROPERTIES 
        OUTPUT_NAME "fort"
)
target_link_libraries(fort-app
    PRIVATE fort)

# Add target to generate docs.
find_program(RONN_EXISTS "ronn")
if(RONN_EXISTS)
    add_custom_target(fort-docs ALL
        COMMAND ronn ${CMAKE_CURRENT_SOURCE_DIR}/docs/fort.md)
else()
    message(WARNING "`ronn` utility is not found. Generation of docs is disabled.")
endif()

# Add tests.
enable_testing()
add_test(
    NAME fort-test
    COMMAND "bash" "-c" "cd ${CMAKE_CURRENT_SOURCE_DIR}/tests && python2 ./test.py --bin-dir=${CMAKE_CURRENT_BINARY_DIR}")