# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

set(boilerplate_build_dir ${CMAKE_CURRENT_BINARY_DIR}/boilerplate)
execute_process(
	COMMAND python "${modCAM_python_SOURCE_DIR}/tools/bindings_boilerplate.py"
		           "${CMAKE_CURRENT_SOURCE_DIR}/py_modcam"
				   "${boilerplate_build_dir}"
				   "modcam"
	COMMAND_ERROR_IS_FATAL ANY
)
file(
	GLOB boilerplate_code "${boilerplate_build_dir}/*.cpp"
)

# CMake documentation recommends against using GLOB to collect a list of source
# files, as the CMakeLists.txt file won't change when a source is added or
# removed, and so the generated build system cannot know when to ask CMake to
# regenerate. In this case, however, scikit-build-core always runs CMake, and so
# there is no danger in using GLOB to collect sources.
file(
	GLOB_RECURSE sources
	LIST_DIRECTORIES TRUE
	RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
	"*.cpp"
)

nanobind_add_module(
	py_modCAM
	STABLE_ABI
	FREE_THREADED
	NB_STATIC
	${boilerplate_code}
	${sources}
)
target_sources(
	py_modCAM PRIVATE
	FILE_SET HEADERS
	BASE_DIRS "${modCAM_python_SOURCE_DIR}/include"
	FILES "${modCAM_python_SOURCE_DIR}/include/default_types.h"
)
set_target_properties(
	py_modCAM PROPERTIES 
	LIBRARY_OUTPUT_NAME "modcam"
)

target_link_libraries(
	py_modCAM 
	PRIVATE 
		Eigen3::Eigen 
		modCAM::mesh 
)

install(
	TARGETS py_modCAM 
	LIBRARY DESTINATION .
)

nanobind_add_stub(
  modcam_stub
  INSTALL_TIME
  MODULE modcam
  OUTPUT modcam/__init__.pyi
  PYTHON_PATH .
  MARKER_FILE modcam/py.typed
)

# We should be able to recurse the submodules with the ``RECURSIVE`` option in
# ``nanobind_add_stub``. However, it doesn't work as expected, and so instead we
# add the submodules individually.
macro(find_submodules result root_dir)
	file(
		GLOB_RECURSE children
		LIST_DIRECTORIES TRUE
		RELATIVE ${root_dir}
		"${root_dir}/*"
	)
	set(dirlist "")
	foreach(child ${children})
		if(IS_DIRECTORY ${root_dir}/${child})
			list(APPEND dirlist ${child})
		endif()
	endforeach()
	set(${result} ${dirlist})
endmacro()
find_submodules(submod_paths "${CMAKE_CURRENT_SOURCE_DIR}/py_modcam")
foreach(submod_path ${submod_paths})
	string(REPLACE "/" "." submod "${submod_path}")
	string(REPLACE "/" "_" submod_tgt "${submod_path}")
	nanobind_add_stub(
	  modcam_${submod_tgt}_stub
	  INSTALL_TIME
	  MODULE modcam.${submod}
	  OUTPUT modcam/${submod_path}/__init__.pyi
	  PYTHON_PATH .
	)
endforeach()
