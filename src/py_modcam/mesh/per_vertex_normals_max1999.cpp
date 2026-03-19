/*
 * This file is part of modCAM, open source software for Computer Aided
 * Manufacturing research.
 *
 * This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at https://mozilla.org/MPL/2.0/.
 *
 * SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
 * SPDX-License-Identifier: MPL-2.0
 */

#include "default_types.h"

#include <modcam/mesh/per_vertex_normals_max1999.h>

#include <nanobind/eigen/dense.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

namespace py = nanobind;
using namespace py::literals;

namespace py_modcam::mesh {

auto per_vertex_normals_max1999(
	const py::DRef<const Eigen::Matrix<double, Eigen::Dynamic, 3,
                                       Eigen::RowMajor>> &vertices,
	const py::DRef<const Eigen::Matrix<int, Eigen::Dynamic, 3, Eigen::RowMajor>>
		&faces)
{
	Eigen::MatrixXN normals;
	modcam::mesh::per_vertex_normals_max1999(normals, vertices, faces);
	return normals;
}

void bind_per_vertex_normals_max1999(py::module_ &m)
{
	m.def("per_vertex_normals_max1999",
	      &py_modcam::mesh::per_vertex_normals_max1999, "vertices"_a, "faces"_a,
	      R"(
Compute the per-vertex normal vectors for a set of vertices and faces, as
described in [max1999]_.

Vertex normals are computed using a weighted sum of their surrounding face
(triangle) normals.

Parameters
----------
vertices : ndarray
    V-by-3 matrix of vertex Cartesian coordinates. Each row specifies a
    vertex's 3D position.
faces : ndarray
    F-by-3 matrix of face (triangle) indices. Each row represents a
    triangle by indexing three vertices (rows) from the `vertices` array.

Returns
-------
ndarray
    V-by-3 matrix of per-vertex normal vectors. If the `vertices` array is
    empty, then an empty array is returned. If the `faces` array is empty,
    then the returned array values are set to NaN.

References
----------
.. [max1999] Nelson Max. Weights for computing vertex normals from facet
             normals. Journal of Graphics Tools, 4:1-6, 1 1999.
)");
}

} // namespace py_modcam::mesh
