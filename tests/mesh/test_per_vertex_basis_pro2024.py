# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

import numpy as np
import modcam.mesh
import pytest


def test_axis_aligned_normal():
    vertex_normals = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
    (b0, b1, b2) = modcam.mesh.per_vertex_basis_pro2024(vertex_normals)
    assert b2 == pytest.approx(vertex_normals)
    assert np.cross(b0, b1) == pytest.approx(b2)
    assert np.cross(b1, b2) == pytest.approx(b0)


def test_non_unit_normal():
    vertex_normals = np.array([[1.0, 1.0, 1.0]])
    (b0, b1, b2) = modcam.mesh.per_vertex_basis_pro2024(vertex_normals)
    unit_normal = vertex_normals / np.linalg.norm(vertex_normals, axis=1, ord=2)
    assert b2 == pytest.approx(unit_normal)
    assert np.cross(b0, b1) == pytest.approx(b2)
    assert np.cross(b1, b2) == pytest.approx(b0)
