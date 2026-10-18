#!/usr/bin/env python3
# Implementer: OpenAI ChatGPT — GPT-6 Astra Pro
"""Software tests, separate from the scientific acceptance gates."""
from dataclasses import replace
from pathlib import Path
from math import pi
import numpy as np
import pytest
import torch
from scipy.spatial.transform import Rotation
from .. import constants as C
from ..mesh import (icosphere, make_system, numpy_geometry, SurfaceQuery,
                    solid_angle_inside, selected_gaps, graph_connected, DTYPE)
from ..energy import Functional, fade
from ..relax import Constraints, relax, ExternalForce
from ..analyse import kabsch, schrodinger_ground_state, _distribution, dual_perimeter
from ..calibrate import singlet_audit
from ..guard import static_audit, TargetFirewall, assert_targets_not_loaded


torch.set_num_threads(C.TORCH_THREADS)


def params():
    return C.Parameters(C.TEST_EAD, C.TEST_E0, C.DELTA_GRID[-1] * C.RP)


@pytest.mark.parametrize('level', [0, C.TEST_SUBDIV, C.SUBDIV, C.CONVERGENCE_SUBDIV])
def test_icosphere_topology(level):
    mesh = icosphere(level)
    assert mesh.n_vertices == 10 * 4 ** level + 2
    assert mesh.n_faces == 20 * 4 ** level
    assert mesh.n_vertices - len(mesh.edges) + mesh.n_faces == 2
    geo = numpy_geometry(mesh.unit_vertices, mesh.faces)
    assert np.all(np.einsum('ij,ij->i', geo['normals'], geo['face_centers']) > 0)
    assert np.allclose(np.linalg.norm(mesh.unit_vertices, axis=1), 1, atol=C.GEOM_TEST_TOL)
    assert np.isclose(geo['vertex_areas'].sum(), geo['face_areas'].sum(), atol=C.GEOM_TEST_TOL)


def test_no_analytic_rest_area_rescaling():
    system = make_system('p', C.SUBDIV)
    assert system.rest_areas.sum() < system.rest_total_area[0]
    assert numpy_geometry(system.initial[0], system.topology.faces)['volume'] < system.rest_volume[0]


def test_volume_translation_invariance():
    mesh = icosphere(C.TEST_SUBDIV)
    shift = np.asarray(C.RAY_DIRECTION)
    a = numpy_geometry(mesh.unit_vertices, mesh.faces)
    b = numpy_geometry(mesh.unit_vertices + shift, mesh.faces)
    assert abs(a['volume'] - b['volume']) < C.GEOM_TEST_TOL


def test_inside_ray_matches_winding_nonconvex():
    mesh = icosphere(C.TEST_SUBDIV)
    vertices = mesh.unit_vertices.copy()
    # A deterministic nonconvex dent, not used in a physics initial geometry.
    mask = vertices[:, -1] > 0
    vertices[mask, -1] *= -1 / 3
    rng = np.random.default_rng(C.TEST_SEED)
    points = rng.uniform(-1, 1, size=vertices.shape)
    q = SurfaceQuery(vertices, mesh)
    assert np.array_equal(q.inside(points), solid_angle_inside(points, vertices, mesh.faces))


def test_signed_gap_outside_inside():
    mesh = icosphere(C.TEST_SUBDIV)
    q = SurfaceQuery(mesh.unit_vertices, mesh)
    center = q.centers[0]; normal = q.normals[0]
    points = np.stack((center + C.PEN_SCALE * normal, center - C.PEN_SCALE * normal))
    selection = q.select(points)
    gaps = selected_gaps(torch.tensor(points), torch.tensor(q.centers), torch.tensor(q.normals), selection).numpy()
    assert gaps[0] > 0 and gaps[1] < 0


def test_outside_no_candidate_has_no_contact():
    system = make_system('p', C.TEST_SUBDIV)
    q = SurfaceQuery(system.initial[0], system.topology)
    point = system.initial[0] + C.CHAIN_EXTRA_DISTANCE * np.asarray(C.RAY_DIRECTION)
    selection = q.select(point)
    gaps = selected_gaps(torch.tensor(point), torch.tensor(q.centers), torch.tensor(q.normals), selection)
    assert torch.all(torch.isinf(gaps))
    assert torch.all(fade(gaps, params().delta, 'linear') == 0)


@pytest.mark.parametrize('shape', ['linear', 'quadratic'])
def test_fade_piecewise_values(shape):
    delta = params().delta
    x = torch.tensor([-delta, 0, delta / 2, delta, 2 * delta], dtype=DTYPE)
    expected = torch.tensor([1, 1, 1 / (4 if shape == 'quadratic' else 2), 0, 0], dtype=DTYPE)
    assert torch.allclose(fade(x, delta, shape), expected)


def test_gap_gradient_includes_target_plane():
    mesh = icosphere(C.TEST_SUBDIV)
    target = torch.tensor(mesh.unit_vertices, dtype=DTYPE, requires_grad=True)
    fi = mesh.faces[0].copy()
    tri = target[fi]
    center = tri.mean(dim=0)
    normal = torch.linalg.cross(tri[1] - tri[0], tri[2] - tri[0]); normal = normal / torch.linalg.vector_norm(normal)
    source = (center.detach() + C.PEN_SCALE * normal.detach())[None].requires_grad_()
    gap = selected_gaps(source, center[None], normal[None], (np.asarray([0]), np.asarray([False])))
    source_grad, target_grad = torch.autograd.grad(gap.sum(), (source, target))
    assert float(torch.linalg.vector_norm(target_grad)) > 0
    assert np.allclose(source_grad.sum(dim=0).numpy() + target_grad.sum(dim=0).numpy(), 0, atol=C.GEOM_TEST_TOL)


@pytest.mark.parametrize('nucleus', ['p', 'D', 'T', 'He3', 'He4'])
def test_autograd_directional_derivative(nucleus):
    system = make_system(nucleus, C.TEST_SUBDIV)
    fun = Functional(system, params())
    rng = np.random.default_rng(C.TEST_SEED)
    x = system.initial + C.TEST_PERTURBATION * rng.normal(size=system.initial.shape)
    direction = rng.normal(size=x.shape); direction /= np.linalg.norm(direction)
    # This checks an ordinary derivative only where both finite-difference
    # endpoints remain on the same candidate/inside/fade branch.
    low = fun.evaluate(x - C.FD_STEP * direction)
    high = fun.evaluate(x + C.FD_STEP * direction)
    for pair in low.pairs:
        for suffix in ('i', 'j'):
            gl, gh = low.pairs[pair]['gap_' + suffix], high.pairs[pair]['gap_' + suffix]
            assert np.array_equal(gl < 0, gh < 0)
            assert np.array_equal(gl < params().delta, gh < params().delta)
    value, gradient = fun.value_and_gradient(x)
    finite_difference = (fun.evaluate(x + C.FD_STEP * direction).energy - fun.evaluate(x - C.FD_STEP * direction).energy) / (2 * C.FD_STEP)
    analytic = float(np.sum(gradient * direction))
    assert abs(finite_difference - analytic) < C.FD_TOL * max(1, abs(finite_difference), abs(analytic))


def test_energy_rigid_invariance():
    system = make_system('He3', C.TEST_SUBDIV)
    fun = Functional(system, params())
    axis = np.asarray(C.ROTATION_AXIS); axis /= np.linalg.norm(axis)
    r = Rotation.from_rotvec(C.ROTATION_ANGLE * axis).as_matrix()
    a = fun.evaluate(system.initial).energy
    b = fun.evaluate(system.initial @ r.T + np.asarray(C.RAY_DIRECTION)).energy
    assert abs(a - b) < C.GEOM_TEST_TOL


def test_adhesion_both_skins_no_half():
    system = make_system('D', C.TEST_SUBDIV)
    p = params(); data = Functional(system, p).evaluate(system.initial).pairs[(0, 1)]
    expected = -p.e0 * (data['area_i'] @ data['weight_i'] + data['area_j'] @ data['weight_j'])
    assert abs(data['adhesion'] - expected) < C.GEOM_TEST_TOL


def test_mesh_only_active_singlet():
    p = params(); system = make_system('D', C.TEST_SUBDIV)
    triplet = Functional(system, p).evaluate(system.initial)
    singlet_sys = make_system('D', C.TEST_SUBDIV, singlet_np=frozenset({(0, 1)}))
    singlet = Functional(singlet_sys, p).evaluate(system.initial)
    assert triplet.pairs[(0, 1)]['contact']
    assert abs(singlet.energy - triplet.energy - C.E_MESH) < C.GEOM_TEST_TOL
    far = system.initial.copy(); far[1] += C.CHAIN_EXTRA_DISTANCE * np.asarray(C.RAY_DIRECTION)
    detached = Functional(singlet_sys, p).evaluate(far)
    assert detached.terms['mesh'] == 0 and detached.terms['slingshot'] == 0


def test_coulomb_uses_vertex_centroids():
    system = make_system('He3', C.TEST_SUBDIV)
    value = Functional(system, params()).evaluate(system.initial)
    centers = system.initial.mean(axis=1)
    assert abs(value.terms['coulomb'] - C.AHC / np.linalg.norm(centers[0] - centers[1])) < C.GEOM_TEST_TOL


def test_graph_gate():
    assert graph_connected(1, {})
    assert graph_connected(3, {(0, 1): True, (1, 2): True, (0, 2): False})
    assert not graph_connected(3, {(0, 1): True, (1, 2): False, (0, 2): False})


def test_global_centroid_projection():
    system = make_system('T', C.TEST_SUBDIV)
    con = Constraints(system.initial)
    q = con.pack(system.initial + np.asarray(C.RAY_DIRECTION))
    x = con.decode(q)
    assert np.allclose(x.mean(axis=(0, 1)), system.initial.mean(axis=(0, 1)), atol=C.GEOM_TEST_TOL)


def test_frozen_capsid_and_system_centroid():
    system = make_system('T', C.TEST_SUBDIV)
    shifted = system.initial[0] + C.Z_GRID[-1] * np.eye(3)[-1]
    con = Constraints(system.initial, frozen={0: shifted})
    x = con.decode(con.pack(system.initial))
    assert np.array_equal(x[0], shifted)
    assert np.allclose(x.mean(axis=(0, 1)), system.initial.mean(axis=(0, 1)), atol=C.GEOM_TEST_TOL)


def test_individual_centroid_constraints():
    system = make_system('D', C.TEST_SUBDIV)
    con = Constraints(system.initial, pin_system=False, pinned_centres={0: np.zeros(3), 1: np.asarray(C.RAY_DIRECTION)})
    x = con.decode(con.pack(system.initial))
    assert np.allclose(x.mean(axis=1), [np.zeros(3), C.RAY_DIRECTION], atol=C.GEOM_TEST_TOL)


def test_isolated_optimizer_is_not_hardcoded_sphere():
    system = make_system('p', C.SUBDIV)
    result = relax(Functional(system, params()))
    assert result.converged
    assert result.gradient_max <= C.GTOL
    # A software regression exposing the specification conflict, not an acceptance pass.
    error = abs(result.evaluation.capsids[0]['volume'] / system.rest_volume[0] - 1)
    assert error > C.ISOLATED_VOLUME_TOL


def test_known_rigid_rotation_kabsch():
    mesh = icosphere(C.TEST_SUBDIV)
    axis = np.asarray(C.ROTATION_AXIS); axis /= np.linalg.norm(axis)
    rotation = Rotation.from_rotvec(C.ROTATION_ANGLE * axis).as_matrix()
    result = kabsch(mesh.unit_vertices, mesh.unit_vertices @ rotation.T)
    assert abs(result['angle_rad'] - C.ROTATION_ANGLE) < C.GEOM_TEST_TOL
    assert np.allclose(result['axis'], axis, atol=C.GEOM_TEST_TOL)


def test_empty_patch_perimeter():
    mesh = icosphere(C.TEST_SUBDIV)
    assert dual_perimeter(mesh.unit_vertices, mesh.faces, np.zeros(mesh.n_vertices, dtype=bool)) == 0
    assert dual_perimeter(mesh.unit_vertices, mesh.faces, np.ones(mesh.n_vertices, dtype=bool)) == 0


def test_measured_patch_not_preset_egg():
    mesh = icosphere(C.TEST_SUBDIV)
    points = mesh.unit_vertices.copy(); points[:, -1] = 0
    weights = np.ones(len(points))
    data = _distribution(points, weights, weights, np.eye(3)[0])
    assert abs(data['aspect_ratio'] - 1) < C.GEOM_TEST_TOL
    assert abs(data['hub_bias']) < C.GEOM_TEST_TOL


def test_unconfined_quantum_mode_is_null():
    result = schrodinger_ground_state(0., 0.)
    assert result['E_zp_MeV'] is None and result['p_rms_MeV_c'] is None


def test_schrodinger_harmonic_ground_state():
    k2 = C.TEST_E0 / C.RP ** 2
    mass = (2 / 3) * (C.MP + C.MN) / 2
    expected = C.HC * np.sqrt(k2 / (2 * mass))
    result = schrodinger_ground_state(k2, 0.)
    assert result['status'] == 'box_and_mesh_converged'
    assert abs(result['E_zp_MeV'] - expected) / expected < C.SCHRODINGER_TOL
    assert abs(result['p_rms_MeV_c'] - np.sqrt(mass * expected)) / np.sqrt(mass * expected) < C.SCHRODINGER_TOL


def test_singlet_inconsistency_is_exposed():
    audit = singlet_audit()
    assert abs(audit['singlet_patch_BE_excluding_sling'] - C.E_SINGLET) < C.GEOM_TEST_TOL
    assert abs(audit['total_singlet_residual'] - 2 * C.Y(2)) < C.GEOM_TEST_TOL


def test_target_firewall():
    assert_targets_not_loaded()
    assert static_audit(Path(__file__).parents[1])['status'] == 'pass'
    guard = TargetFirewall()
    with pytest.raises(ImportError):
        guard.find_spec('held_out.targets')


def test_force_work_has_declared_total_force():
    system = make_system('T', C.TEST_SUBDIV)
    x = torch.tensor(system.initial, requires_grad=True)
    weights = numpy_geometry(system.initial[0], system.topology.faces)['vertex_areas']
    weights /= weights.sum()
    force = C.FORCE_STEP * np.asarray(C.RAY_DIRECTION)
    external = ExternalForce(0, force, weights)
    gradient, = torch.autograd.grad(external.work_potential(x), x)
    assert np.allclose(-gradient[0].sum(dim=0).numpy(), force, atol=C.GEOM_TEST_TOL)
    assert np.allclose(gradient[1:].numpy(), 0, atol=C.GEOM_TEST_TOL)
