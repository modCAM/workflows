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


@pytest.fixture
def icosahedron():
    r = 2.0 * np.sqrt(5.0) / 5.0
    zenith_angle = np.zeros((12, 1))
    zenith_angle[1:6, 0] = np.asin(r)
    zenith_angle[6:11, 0] = np.pi - np.asin(r)
    zenith_angle[11] = np.pi
    azimuth = np.zeros((12, 1))
    azimuth[1:6, 0] = np.linspace(0.0, 8.0 * np.pi / 5.0, 5)
    azimuth[6:11, 0] = np.linspace(np.pi / 5.0, 9.0 * np.pi / 5.0, 5)

    vertices = np.zeros((12, 3))
    vertices[:, [0]] = np.sin(zenith_angle) * np.cos(azimuth)
    vertices[:, [1]] = np.sin(zenith_angle) * np.sin(azimuth)
    vertices[:, [2]] = np.cos(zenith_angle)

    faces = np.array(
        [
            [0, 1, 2],
            [0, 2, 3],
            [0, 3, 4],
            [0, 4, 5],
            [0, 5, 1],
            [2, 1, 6],
            [3, 2, 7],
            [4, 3, 8],
            [5, 4, 9],
            [1, 5, 10],
            [6, 7, 2],
            [7, 8, 3],
            [8, 9, 4],
            [9, 10, 5],
            [10, 6, 1],
            [11, 7, 6],
            [11, 8, 7],
            [11, 9, 8],
            [11, 10, 9],
            [11, 6, 10],
        ]
    )

    return (vertices, faces)


def test_icosahedron(icosahedron):
    vertices = icosahedron[0]
    faces = icosahedron[1]
    vertex_normals = modcam.mesh.per_vertex_normals_max1999(vertices, faces)
    assert vertex_normals.shape == vertices.shape
    assert vertex_normals == pytest.approx(vertices)


def test_partial_icosahedron(icosahedron):
    vertices = icosahedron[0]
    faces = icosahedron[1][0:5, :]
    vertex_normals = modcam.mesh.per_vertex_normals_max1999(vertices, faces)
    assert vertex_normals.shape == vertices.shape
    assert not np.isnan(vertex_normals[0:6, :]).any()
    assert np.isnan(vertex_normals[6:, :]).all()


def test_empty_face_array(icosahedron):
    vertices = icosahedron[0]
    faces = np.empty((0, 3))
    vertex_normals = modcam.mesh.per_vertex_normals_max1999(vertices, faces)
    assert vertex_normals.shape == vertices.shape
    assert np.isnan(vertex_normals).all()


def test_empty_vertex_array(icosahedron):
    vertices = np.empty((0, 3))
    faces = icosahedron[1]
    vertex_normals = modcam.mesh.per_vertex_normals_max1999(vertices, faces)
    assert vertex_normals.shape == vertices.shape
