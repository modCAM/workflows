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

#include <modcam/mesh/per_vertex_basis_pro2024.h>

#include <nanobind/eigen/dense.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>

namespace py = nanobind;
using namespace py::literals;

namespace py_modcam::mesh {

auto per_vertex_basis_pro2024(
	const py::DRef<const Eigen::Matrix<double, Eigen::Dynamic, 3,
                                       Eigen::RowMajor>> &vertex_normals)
{
	std::tuple<Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>,
	           Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>,
	           Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor>>
		result;
	Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor> &b0 =
		std::get<0>(result);
	Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor> &b1 =
		std::get<1>(result);
	Eigen::Matrix<double, Eigen::Dynamic, 3, Eigen::RowMajor> &b2 =
		std::get<2>(result);
	modcam::mesh::per_vertex_basis_pro2024(b0, b1, b2, vertex_normals);
	return result;
}

void bind_per_vertex_basis_pro2024(py::module_ &m)
{
	m.def("per_vertex_basis_pro2024",
	      &py_modcam::mesh::per_vertex_basis_pro2024, "vertex_normals"_a,
	      R"(
Compute an orthonormal set of basis vectors for each vertex in a mesh.
Algorithm by [pro2024]_.

Each vertex in the mesh is assigned a local coordinate system, where the
z-axis is aligned with the vertex normal.

Parameters
----------
vertex_normals : ndarray
    V-by-3 matrix of mesh vertex 3D normals

Returns
-------
b0 : ndarray
    V-by-3 matrix of basis vectors, corresponding to the vertex-local
    x-axis.
b1 : ndarray
    V-by-3 matrix of basis vectors, corresponding to the vertex-local
    y-axis.
b2 : ndarray
    V-by-3 matrix of basis vectors, corresponding to the vertex-local
    z-axis (aligned with the vertex normal).

References
----------
.. [pro2024] prosilio. Per-vertex basis. GitHub, 2024.
)");
}

} // namespace py_modcam::mesh
