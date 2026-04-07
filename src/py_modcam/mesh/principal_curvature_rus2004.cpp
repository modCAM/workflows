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

#include <modcam/mesh/principal_curvature_rus2004.h>

#include <nanobind/eigen/dense.h>
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <nanobind/stl/tuple.h>

namespace py = nanobind;
using namespace py::literals;

namespace py_modcam::mesh {

auto principal_curvature_rus2004(
	const py::DRef<const Eigen::Matrix<double, Eigen::Dynamic, 3,
                                       Eigen::RowMajor>> &vertices,
	const py::DRef<const Eigen::Matrix<int, Eigen::Dynamic, 3, Eigen::RowMajor>>
		&faces)
{
	std::tuple<Eigen::MatrixXN, Eigen::MatrixXN, Eigen::VectorXN,
	           Eigen::VectorXN>
		result;
	Eigen::MatrixXN &pd1 = std::get<0>(result);
	Eigen::MatrixXN &pd2 = std::get<1>(result);
	Eigen::VectorXN &pv1 = std::get<2>(result);
	Eigen::VectorXN &pv2 = std::get<3>(result);
	modcam::mesh::principal_curvature_rus2004(pd1, pd2, pv1, pv2, vertices,
	                                          faces);
	return result;
}

void bind_principal_curvature_rus2004(py::module_ &m)
{
	m.def("principal_curvature_rus2004",
	      &py_modcam::mesh::principal_curvature_rus2004, "vertices"_a,
	      "faces"_a,
	      R"(
Compute the (per-vertex) principal curvature on a triangle mesh using the
algorithm described in [rus2004]_.

While many principal curvature algorithms use a tunable "neighborhood" to
compute their estimates, this algorithm uses only 1-ring vertex
neighborhoods. Although the algorithm in [rus2004]_ can be used to compute
curvature derivates, that is not done here.

If the `vertices` array is empty, then all returned arrays are empty. If
the `faces` array is empty, then all returned array values are set to NaN.

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
pd1 : ndarray
    V-by-3 maximal curvature direction for each vertex.
pd2 : ndarray
    V-by-3 minimal curvature direction for each vertex.
pv1 : ndarray
    V-by-1 maximal curvature value for each vertex.
pv2 : ndarray
    V-by-1 minimal curvature value for each vertex.

References
----------
.. [rus2004] S. Rusinkiewicz. Estimating curvatures and their derivatives
             on triangle meshes. pages 486-493. IEEE, 2004.
)");
}

} // namespace py_modcam::mesh
