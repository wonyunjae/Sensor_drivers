
find_package(PkgConfig)
pkg_check_modules(
    MY_LIBUSB
    IMPORTED_TARGET
    libusb-1.0
)

## XS COMMON

file(
    GLOB XSCOMMON_SRC_FILES
    xscommon/*.c xscommon/*.cpp xscommon/*.h
)

add_library(
    xscommon
    STATIC
    ${XSCOMMON_SRC_FILES}
)

# Note: use 'SHELL:' prefix to prevent option de-duplication here:
target_compile_options(
    xscommon
    PRIVATE
    "SHELL:-include xstypes/xsens_compat.h"
    "SHELL:-include xscommon_config.h"
)

target_compile_definitions(
    xscommon
    PRIVATE
    -DXSENS_DEBUG
)

set_target_properties(
    xscommon
    PROPERTIES
    CXX_STANDARD 11
    POSITION_INDEPENDENT_CODE ON
)

target_include_directories(
    xscommon
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    xscommon
)

## XS CONTROLLER

file(
    GLOB XSCONTROLLER_SRC_FILES
    xscontroller/*.c xscontroller/*.cpp xscontroller/*.h
)

add_library(
    xscontroller
    STATIC
    ${XSCONTROLLER_SRC_FILES}
)

target_compile_options(
    xscontroller
    PRIVATE
    "SHELL:-include xscontrollerconfig.h"
)

target_compile_definitions(
    xscontroller
    PRIVATE
    -DHAVE_JOURNALLER
    -DXSENS_DEBUG
)

if(${MY_LIBUSB_FOUND})
    target_compile_definitions(
        xscontroller
        PRIVATE
        -DHAVE_LIBUSB
    )
endif()

set_target_properties(
    xscontroller
    PROPERTIES
    CXX_STANDARD 11
    POSITION_INDEPENDENT_CODE ON
)

target_include_directories(
    xscontroller
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    xscontroller
)

# XS TYPES

file(
    GLOB SRC_FILES
    xstypes/*.c xstypes/*.cpp xstypes/*.h
)

list(REMOVE_ITEM ${SRC_FILES} xstypes/xstypesdynlib.c)

add_library(
    xstypes
    STATIC
    ${SRC_FILES}
)

set_target_properties(
    xstypes
    PROPERTIES
    CXX_STANDARD 11
    POSITION_INDEPENDENT_CODE ON
)

target_include_directories(
    xstypes
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_compile_definitions(
    xstypes
    PRIVATE
    -DXSENS_DEBUG
)
