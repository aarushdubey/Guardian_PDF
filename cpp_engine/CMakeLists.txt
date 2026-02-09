cmake_minimum_required(VERSION 3.15)
project(guardian_pdf_engine VERSION 1.0.0 LANGUAGES CXX)

# C++ Standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Find dependencies
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

# Try to find poppler-cpp via pkg-config
find_package(PkgConfig REQUIRED)
pkg_check_modules(POPPLER REQUIRED poppler-cpp)

# Main library sources
set(SOURCES
    src/PDFShredder.cpp
    src/TextChunker.cpp
    src/RabinKarpDedup.cpp
)

# Python module
pybind11_add_module(pdf_shredder 
    src/bindings.cpp
    ${SOURCES}
)

# Include directories
target_include_directories(pdf_shredder PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${POPPLER_INCLUDE_DIRS}
)

# Link directories and libraries
target_link_directories(pdf_shredder PRIVATE
    ${POPPLER_LIBRARY_DIRS}
)

target_link_libraries(pdf_shredder PRIVATE
    ${POPPLER_LIBRARIES}
)

# Compiler warnings
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    target_compile_options(pdf_shredder PRIVATE
        -Wall -Wextra -Wpedantic
    )
endif()

# Tests (optional - only if Catch2 is found)
find_package(Catch2 QUIET)
if(Catch2_FOUND)
    enable_testing()
    
    add_executable(test_pdfshredder
        tests/test_pdfshredder.cpp
        ${SOURCES}
    )
    
    target_include_directories(test_pdfshredder PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/src
        ${POPPLER_INCLUDE_DIRS}
    )
    
    target_link_directories(test_pdfshredder PRIVATE
        ${POPPLER_LIBRARY_DIRS}
    )
    
    target_link_libraries(test_pdfshredder PRIVATE
        Catch2::Catch2
        ${POPPLER_LIBRARIES}
    )
    
    include(CTest)
    include(Catch)
    catch_discover_tests(test_pdfshredder)
    
    message(STATUS "Tests enabled - Catch2 found")
else()
    message(STATUS "Tests disabled - Catch2 not found (install with: brew install catch2)")
endif()

# Installation
install(TARGETS pdf_shredder
    LIBRARY DESTINATION .
)
