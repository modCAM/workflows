# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
# 
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
# 
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

#[=======================================================================[.rst:
bind_submodule
--------------

Generate binding code.

Functions
^^^^^^^^^

.. command:: bind_submodule

  Description

  .. code-block:: cmake

    bind_submodule(submodule_name
		SOURCES src1 [src2...]
		DESCRIPTION <description>)

  More description

  ``SOURCES``
    Specify source files to be included in the submodule.

  ``DESCRIPTION``
    A short description of the submodule.

#]=======================================================================]

include_guard(GLOBAL)

set_property(GLOBAL PROPERTY submodule_bindings)

function(get_global_var var_name value)
	get_property(${value} GLOBAL PROPERTY ${var_name})
	return(PROPAGATE ${value})
endfunction()

function(set_global_var var_name value)
	set_property(GLOBAL PROPERTY ${var_name} "${value}")
endfunction()

macro(subdirlist result curdir)
	file(GLOB children ${curdir}/*)
	set(dirlist "")
	foreach(child ${children})
		if(IS_DIRECTORY ${child})
			list(APPEND dirlist ${child})
		endif()
	endforeach()
	set(${result} ${dirlist})
endmacro()

function(binding_decls sources decls)
	# Function declarations of the form
	# ``void bind_<function>(py::module_ &m);``
	list(
		TRANSFORM sources
		REPLACE "\.cpp$" ""
		OUTPUT_VARIABLE ${decls}
	)
	list(
		TRANSFORM ${decls}
		PREPEND "void bind_"
	)
	list(
		TRANSFORM ${decls}
		APPEND "(py::module_ &m)"
	)
	list(JOIN ${decls} ";\n" ${decls})
	string(APPEND ${decls} ";")
	return(PROPAGATE ${decls})
endfunction()

function(binding_funcs sources funcs)
	# Function invocations of the form
	# ``bind_<function>(m);``
	list(
		TRANSFORM sources
		REPLACE "\.cpp$" ""
		OUTPUT_VARIABLE ${funcs}
	)
	list(
		TRANSFORM ${funcs}
		PREPEND "bind_"
	)
	list(
		TRANSFORM ${funcs}
		APPEND "(m)"
	)
	list(JOIN ${funcs} ";\n" ${funcs})
	string(APPEND ${funcs} ";")
	return(PROPAGATE ${funcs})
endfunction()

function(bind_submodule submodule_name)
	# CMake documentation recommends against using GLOB to collect a list of
	# source files, as the CMakeLists.txt file won't change when a source is
	# added or removed, and so the generated build system cannot know when to
	# ask CMake to regenerate. In this case, however, scikit-build-core always
	# runs CMake, and so there is no danger in using GLOB to collect sources.
	file(
		GLOB submodule_sources
		LIST_DIRECTORIES false
		RELATIVE ${CMAKE_CURRENT_SOURCE_DIR}
		"*.cpp"
	)
	target_sources(
		py_modCAM PRIVATE
		${submodule_sources}
	)

	binding_decls("${submodule_sources}" submodule_binding_decls)
	binding_funcs("${submodule_sources}" submodule_binding_funcs)
	string(
		CONCAT binding_code
		"#include <nanobind/nanobind.h>\n"
		"namespace py = nanobind;\n"
		"${submodule_binding_decls}\n"
		"void bind_${submodule_name}(py::module_ &m) {\n"
		"${submodule_binding_funcs}\n"
		"}\n"
	)
	file(
		CONFIGURE OUTPUT bind_${submodule_name}.cpp
		CONTENT "${binding_code}"
	)
	target_sources(
		py_modCAM PRIVATE
		${CMAKE_CURRENT_BINARY_DIR}/${submodule_name}.cpp
	)
endfunction()

function(add_submodule module_target)
	set(prefix ARG)
	set(no_value_keywords "")
	set(single_value_keywords SUBMODULE DESCRIPTION BASE_DIRECTORY)
	set(multi_value_keywords "")
	cmake_parse_arguments(
		PARSE_ARGV 1
		${prefix}
		"${no_value_keywords}" "${single_value_keywords}" "${multi_value_keywords}"
	)
	
	if(NOT ${prefix}_BASE_DIRECTORY)
		set(${prefix}_BASE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
	endif()

	bind_submodule(${${prefix}_SUBMODULE})

	# Generate bind_${submodule}() function code, and add it to global bindings variable.
	string(
		CONCAT binding_code
		"#include <nanobind/nanobind.h>\n"
		"namespace py = nanobind;\n"
		"void bind_mesh(py::module_ &);\n"
		"NB_MODULE(modcam, m) {\n"
		"m.doc() = \"Open source software for Computer Aided Manufacturing (CAM) research\";\n"
		"py::module_ mesh_m = m.def_submodule(\"mesh\", \"Tools to work with triangle mesh data\");\n"
		"bind_mesh(mesh_m);\n"
		"}\n"
	)
endfunction()

function(configure_python_module module_name)
	set(prefix ARG)
	set(no_value_keywords "")
	set(single_value_keywords DESCRIPTION BASE_DIRECTORY)
	set(multi_value_keywords "")
	cmake_parse_arguments(
		PARSE_ARGV 1
		${prefix}
		"${no_value_keywords}" "${single_value_keywords}" "${multi_value_keywords}"
	)
endfunction()

