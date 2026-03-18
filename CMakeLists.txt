# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

cmake_minimum_required(VERSION 4.0)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/tools/cmake")

project(
	modCAM_python
	DESCRIPTION "Python bindings for the modCAM Computer Aided Manufacturing (CAM) research software"
	LANGUAGES CXX
)

if (NOT SKBUILD)
	message(WARNING "\
	This CMake file is meant to be executed using 'scikit-build'. Running
	it directly will almost certainly not produce the desired result. If
	you are a user trying to install this package, please use the command
	below, which will install all necessary build dependencies, compile
	the package in an isolated environment, and then install it.
	=====================================================================
	$ pip install .
	=====================================================================
	If you are a software developer, and this is your own package, then
	it is usually much more efficient to install the build dependencies
	in your environment once and use the following command that avoids
	a costly creation of a new virtual environment at every compilation:
	=====================================================================
	$ pip install nanobind scikit-build-core[pyproject]
	$ pip install --no-build-isolation -ve .
	=====================================================================
	You may optionally add -Ceditable.rebuild=true to auto-rebuild when
	the package is imported. Otherwise, you need to re-run the above
	after editing C++ files.")
endif()

# Helpful CMake modules
include(GNUInstallDirs)

# Require out-of-source builds
file(TO_CMAKE_PATH "${PROJECT_BINARY_DIR}/CMakeLists.txt" LOC_PATH)
if(PROJECT_IS_TOP_LEVEL AND EXISTS "${LOC_PATH}")
	message(FATAL_ERROR "You cannot build in a source directory (or any directory with a CMakeLists.txt file). Please make a build directory. Feel free to remove CMakeCache.txt and CMakeFiles.")
endif()

# Require a minimum C++ standard, but let a parent project ask for something
# higher.
set(MODCAM_MIN_CXX_STANDARD 20)
if(DEFINED CMAKE_CXX_STANDARD)
	if(CMAKE_CXX_STANDARD EQUAL 98 OR CMAKE_CXX_STANDARD LESS MODCAM_MIN_CXX_STANDARD)
		message(FATAL_ERROR "modCAM requires at least C++${MODCAM_MIN_CXX_STANDARD}")
	endif()
else()
	set(CMAKE_CXX_STANDARD ${MODCAM_MIN_CXX_STANDARD})
endif()

# Always enforce the language constraint
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# We don't need compiler extensions, but let a parent ask for them
if(NOT DEFINED CMAKE_CXX_EXTENSIONS)
	set(CMAKE_CXX_EXTENSIONS OFF)
endif()

# Dependencies
find_package(Eigen3 REQUIRED NO_MODULE)
find_package(libigl CONFIG REQUIRED)

include(zero_pad_version)
zero_pad_version(${SKBUILD_PROJECT_VERSION} version_tag)
include(FetchContent)
FetchContent_Declare(
    modCAM
    GIT_REPOSITORY https://github.com/modCAM/modcam.git
	GIT_TAG "${version_tag}"
	GIT_SHALLOW TRUE
	GIT_PROGRESS TRUE
	FIND_PACKAGE_ARGS
)
FetchContent_MakeAvailable(modCAM)
find_package(
	Python 3.9
	REQUIRED COMPONENTS Development.Module
	OPTIONAL_COMPONENTS Development.SABIModule
)
execute_process(
	COMMAND "${Python_EXECUTABLE}" -m nanobind --cmake_dir
	OUTPUT_STRIP_TRAILING_WHITESPACE
	OUTPUT_VARIABLE nanobind_ROOT
)
find_package(nanobind CONFIG REQUIRED)

# Project files
add_subdirectory(src)
