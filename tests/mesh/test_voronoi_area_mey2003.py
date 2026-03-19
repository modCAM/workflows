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


def test_equilateral_triangle():
    vertices = np.array(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, np.sqrt(3.0) / 2.0, 0.0]]
    )
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert weights == pytest.approx(np.sqrt(3.0) / 12.0)


def test_obtuse_triangle():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert (weights == np.array([[0.0125, 0.0125, 0.025]])).all()


def test_multiple_triangles():
    vertices = np.array(
        [
            [0.0, 0.0, 0.0],
            [1.0, 0.0, 0.0],
            [0.5, np.sqrt(3.0) / 2.0, 0.0],
            [0.5, 0.1, 0.0],
        ]
    )
    faces = np.array([[0, 1, 2], [0, 1, 3]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert weights.shape == (faces.shape[0], 3)
    one_third_area = np.sqrt(3.0) / 12.0
    assert weights == pytest.approx(
        np.array(
            [[one_third_area, one_third_area, one_third_area], [0.0125, 0.0125, 0.025]]
        )
    )


def test_colocated_vertices():
    vertices = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert (weights == 0.0).all()


def test_face_singularity():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
    faces = np.array([[0, 0, 0]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert (weights == 0.0).all()


def test_colinear_vertices():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.0, 0.0]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert (weights == 0.0).all()


def test_empty_face_array():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
    faces = np.empty((0, 3))
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert weights.size == 0


def test_empty_vertex_array():
    vertices = np.empty((0, 3))
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert (weights == 0.0).all()


def test_2D_vertex_array():
    vertices = np.array([[0.0, 0.0], [1.0, 0.0], [0.5, 0.1]])
    faces = np.array([[0, 1, 2]])
    weights = modcam.mesh.voronoi_area_mey2003(vertices, faces)
    assert (weights == np.array([[0.0125, 0.0125, 0.025]])).all()


def test_improperly_sized_face_array():
    with pytest.raises(TypeError):
        vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.1, 0.0]])
        faces = np.array([[0, 1]])
        modcam.mesh.voronoi_area_mey2003(vertices, faces)
