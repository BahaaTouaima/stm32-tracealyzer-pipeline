cmake_minimum_required(VERSION 3.10)
project(stm32_tracealyzer_pipeline NONE)
#this wraps the existing Makefile-based firmware build.
#its lets Cmake trigger 'make' inside firmware/build/gcc
#so the whole project can be built with 'cmake --build'
add_custom_target(firmware ALL
COMMAND make -C ${CMAKE_SOURCE_DIR}/firmware/build/gcc
COMMENT "Building FreeRTOS firmware via existing Makefile"
)
