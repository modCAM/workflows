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
zero_pad_version
----------------

Add zero padding to version numbers. When the version is retrieved from
scikit-build-core, zero-prefixed numbers have the zeros removed. This function
adds those zeros back. For example, 2026.1.1 --> 2026.01.01

Functions
^^^^^^^^^

.. command:: zero_pad_version

  Description

  .. code-block:: cmake

    zero_pad_version(version_str zero_padded_version)

#]=======================================================================]

include_guard(GLOBAL)

function(zero_pad_version version_str zero_padded_version)
	string(REPLACE "." ";" version_list ${version_str})
	list(GET version_list 0 version_year)
	list(GET version_list 1 version_month)
	string(LENGTH ${version_month} version_month_len)
	if(version_month_len LESS 2)
		string(PREPEND version_month 0)
	endif()
	list(GET version_list 2 version_day)
	string(LENGTH ${version_day} version_day_len)
	if(version_day_len LESS 2)
		string(PREPEND version_day 0)
	endif()
	set(${zero_padded_version} "${version_year}.${version_month}.${version_day}")
	return(PROPAGATE ${zero_padded_version})
endfunction()
