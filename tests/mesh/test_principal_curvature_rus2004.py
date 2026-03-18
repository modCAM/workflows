# This file is part of modCAM, open source software for Computer Aided
# Manufacturing research.
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# SPDX-FileCopyrightText: Copyright contributors to the modCAM project.
# SPDX-License-Identifier: MPL-2.0

import igl
import numpy as np
import modcam.mesh
import pooch
import pytest


@pytest.fixture
def sphere_mesh():
    sphere_file = pooch.retrieve(
        url="https://github.com/modCAM/modcam-data/raw/main/mesh/sphere.stl",
        known_hash="sha256:502ed3c6aa892e0ff4e7d36ae575ce0e44bf564df6c208a0a8cf924299432109",
    )
    vertices, faces = igl.read_triangle_mesh(sphere_file)
    vertices, _, _, faces = igl.remove_duplicate_vertices(vertices, faces, 1.0e-7)
    for i in range(3):
        center = (vertices[:, i].max() - vertices[:, i].min()) / 2.0
        vertices[:, i] -= center
    vertices /= np.linalg.norm(vertices, ord=2, axis=1, keepdims=True)
    radius = 11.37
    vertices *= radius
    return vertices, faces, radius


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

    return vertices, faces


@pytest.fixture
def cylinder():
    radius = 0.5
    x0 = radius
    x1 = radius * np.cos(1.0 * 2.0 * np.pi / 6.0)
    x2 = radius * np.cos(2.0 * 2.0 * np.pi / 6.0)
    x3 = radius * np.cos(3.0 * 2.0 * np.pi / 6.0)
    x4 = radius * np.cos(4.0 * 2.0 * np.pi / 6.0)
    x5 = radius * np.cos(5.0 * 2.0 * np.pi / 6.0)
    y0 = 0.0
    y1 = radius * np.sin(1.0 * 2.0 * np.pi / 6.0)
    y2 = radius * np.sin(2.0 * 2.0 * np.pi / 6.0)
    y3 = radius * np.sin(3.0 * 2.0 * np.pi / 6.0)
    y4 = radius * np.sin(4.0 * 2.0 * np.pi / 6.0)
    y5 = radius * np.sin(5.0 * 2.0 * np.pi / 6.0)
    vertices = np.array(
        [
            [x0, y0, 0.0],
            [x0, y0, 1.0],
            [x1, y1, 0.0],
            [x1, y1, 1.0],
            [x2, y2, 0.0],
            [x2, y2, 1.0],
            [x3, y3, 0.0],
            [x3, y3, 1.0],
            [x4, y4, 0.0],
            [x4, y4, 1.0],
            [x5, y5, 0.0],
            [x5, y5, 1.0],
        ]
    )
    faces = np.array(
        [
            [1, 0, 2],
            [2, 3, 1],
            [3, 2, 4],
            [4, 5, 3],
            [5, 4, 6],
            [6, 7, 5],
            [7, 6, 8],
            [8, 9, 7],
            [9, 8, 10],
            [10, 11, 9],
            [11, 10, 0],
            [0, 1, 11],
        ]
    )
    return vertices, faces, radius


def test_sphere_principal_curvature(sphere_mesh):
    vertices = sphere_mesh[0]
    faces = sphere_mesh[1]
    pd1, pd2, pv1, pv2 = modcam.mesh.principal_curvature_rus2004(vertices, faces)
    radius = sphere_mesh[2]
    assert len(pv1.shape) == 1
    assert pv1.shape[0] == vertices.shape[0]
    assert len(pv2.shape) == 1
    assert pv2.shape[0] == vertices.shape[0]
    assert pd1.shape[0] == vertices.shape[0]
    assert pd1.shape[1] == 3
    assert pd2.shape[0] == vertices.shape[0]
    assert pd2.shape[1] == 3
    assert pv1 == pytest.approx(1.0 / radius)
    assert pv2 == pytest.approx(1.0 / radius)


def test_empty_face_array():
    vertices = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]])
    faces = np.empty((0, 3))
    pd1, pd2, pv1, pv2 = modcam.mesh.principal_curvature_rus2004(vertices, faces)
    assert len(pv1.shape) == 1
    assert pv1.shape[0] == vertices.shape[0]
    assert len(pv2.shape) == 1
    assert pv2.shape[0] == vertices.shape[0]
    assert pd1.shape[0] == vertices.shape[0]
    assert pd1.shape[1] == 3
    assert pd2.shape[0] == vertices.shape[0]
    assert pd2.shape[1] == 3
    assert np.isnan(pv1).all()
    assert np.isnan(pv2).all()
    assert np.isnan(pd1).all()
    assert np.isnan(pd2).all()


def test_empty_vertex_array():
    vertices = np.empty((0, 3))
    faces = np.array([[0, 1, 2]])
    pd1, pd2, pv1, pv2 = modcam.mesh.principal_curvature_rus2004(vertices, faces)
    assert (pv1.size, pv2.size, pd1.size, pd2.size) == (0, 0, 0, 0)


def test_icosahedron(icosahedron):
    vertices = icosahedron[0]
    faces = icosahedron[1]
    pd1, pd2, pv1, pv2 = modcam.mesh.principal_curvature_rus2004(vertices, faces)
    assert len(pv1.shape) == 1
    assert pv1.shape[0] == vertices.shape[0]
    assert len(pv2.shape) == 1
    assert pv2.shape[0] == vertices.shape[0]
    assert pd1.shape[0] == vertices.shape[0]
    assert pd1.shape[1] == 3
    assert pd2.shape[0] == vertices.shape[0]
    assert pd2.shape[1] == 3
    assert pv1 == pytest.approx(1.0)
    assert pv2 == pytest.approx(1.0)


def test_cylinder(cylinder):
    vertices = cylinder[0]
    faces = cylinder[1]
    pd1, pd2, pv1, pv2 = modcam.mesh.principal_curvature_rus2004(vertices, faces)
    assert len(pv1.shape) == 1
    assert pv1.shape[0] == vertices.shape[0]
    assert len(pv2.shape) == 1
    assert pv2.shape[0] == vertices.shape[0]
    assert pd1.shape[0] == vertices.shape[0]
    assert pd1.shape[1] == 3
    assert pd2.shape[0] == vertices.shape[0]
    assert pd2.shape[1] == 3
    assert pv1 == pytest.approx(0.0)
    radius = cylinder[2]
    assert pv2 == pytest.approx(1.0 / radius)
    assert pd1[:, 0:2] == pytest.approx(0.0)
    assert np.abs(pd1[:, 2]) == pytest.approx(1.0)
    assert pd2[:, 2] == pytest.approx(0.0)
    assert np.sqrt(pd2[:, 0] * pd2[:, 0] + pd2[:, 1] * pd2[:, 1]) == pytest.approx(1.0)
