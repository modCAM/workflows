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

#include <modcam/mesh/voronoi_area_mey2003.h>

#include <nanobind/eigen/dense.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>

namespace py = nanobind;
using namespace py::literals;

namespace py_modcam::mesh {

auto voronoi_area_mey2003(
	const py::DRef<const Eigen::MatrixXN> &vertices,
	const py::DRef<const Eigen::Matrix<int, Eigen::Dynamic, 3, Eigen::RowMajor>>
		&faces)
{
	if (vertices.cols() > 3 || vertices.cols() < 2) {
		throw py::type_error("vertices must have two or three columns.");
	}
	Eigen::MatrixXN v_area;
	modcam::mesh::voronoi_area_mey2003(v_area, vertices, faces);
	return v_area;
}

void bind_voronoi_area_mey2003(py::module_ &m)
{
	m.def("voronoi_area_mey2003", &py_modcam::mesh::voronoi_area_mey2003,
	      "vertices"_a, "faces"_a,
	      R"(
Compute the Voronoi cell areas for the triangles in a mesh as described in
[mey2003]_.

For a non-obtuse triangle, the Voronoi areas are bounded by segments
connecting the triangle's circumcenter to the midpoints of its edges. In
the case of an obtuse triangle, we replace the triangle circumcenter with
the midpoint of the edge opposite the obtuse angle.

Parameters
----------
vertices : ndarray
    V-by-3 (or V-by-2) matrix of vertex Cartesian coordinates. Each row
    specifies a vertex's 3D (or 2D) position.
faces : ndarray
    F-by-3 matrix of face (triangle) indices. Each row represents a
    triangle by indexing three vertices (rows) from the `vertices` array.

Returns
-------
ndarray
    F-by-3 matrix of the Voronoi area of each vertex in each triangle. Each
    value in this array corresponds to a triangle corner in the `faces`
    array. If the `faces` array is empty, then an empty array is returned.
    If the `vertices` array is empty, then the returned array values are
    set to zero.

References
----------
.. [mey2003] Mark Meyer, Mathieu Desbrun, Peter Schröder, and Alan H. Barr.
             Discrete differential-geometry operators for triangulated
             2-manifolds, 2003.
)");
}

} // namespace py_modcam::mesh
