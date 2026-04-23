import numpy as np

from core import (
    VKernelAPI,
    VKernelConfig,
    VKernelEngine,
    build_canonical_graph,
    make_cluster_input,
    make_radial_input,
    make_ring_input,
)


def test_build_canonical_graph_has_19_nodes():
    graph = build_canonical_graph()
    assert graph.number_of_nodes() == 19
    assert graph.number_of_edges() > 0


def test_engine_returns_valid_result():
    graph = build_canonical_graph()
    engine = VKernelEngine(graph, VKernelConfig(steps=10))

    x = make_radial_input(graph, seed=42)
    result = engine.compute(x)

    assert result.final_state.shape == (19,)
    assert result.mode_coefficients.shape[0] == 19
    assert result.coefficient_history.shape[0] == 11  # steps + initial
    assert 0 <= result.dominant_mode < 19
    assert result.dominant_coefficient >= 0.0


def test_engine_final_state_is_finite():
    graph = build_canonical_graph()
    engine = VKernelEngine(graph, VKernelConfig(steps=20))

    x = make_ring_input(graph, seed=7)
    result = engine.compute(x)

    assert np.all(np.isfinite(result.final_state))
    assert np.all(np.isfinite(result.mode_coefficients))
    assert np.all(np.isfinite(result.coefficient_history))


def test_input_shapes_are_preserved():
    graph = build_canonical_graph()
    engine = VKernelEngine(graph)

    x = make_cluster_input(graph, seed=11)
    result = engine.compute(x)

    assert result.trajectory.ndim == 2
    assert result.trajectory.shape[1] == 19


def test_reproducible_same_input_same_result():
    graph = build_canonical_graph()
    config = VKernelConfig(steps=30)

    engine1 = VKernelEngine(graph, config)
    engine2 = VKernelEngine(graph, config)

    x = make_radial_input(graph, seed=123)

    r1 = engine1.compute(x)
    r2 = engine2.compute(x)

    assert r1.dominant_mode == r2.dominant_mode
    assert np.allclose(r1.final_state, r2.final_state)
    assert np.allclose(r1.mode_coefficients, r2.mode_coefficients)


def test_api_run_radial_returns_summary():
    api = VKernelAPI()
    result = api.run_radial(noise=0.05, seed=42)

    summary = result.summary()

    assert isinstance(summary, str)
    assert "Mode" in summary
    assert result.classification.label != ""
    assert result.classification.confidence >= 0.0


def test_api_run_ring_and_cluster_produce_valid_modes():
    api = VKernelAPI()

    ring_result = api.run_ring(noise=0.05, seed=1)
    cluster_result = api.run_cluster(
        hot_nodes=[2, 4, 8, 11],
        cold_nodes=[1, 6, 13],
        noise=0.05,
        seed=2,
    )

    assert 0 <= ring_result.engine_result.dominant_mode < 19
    assert 0 <= cluster_result.engine_result.dominant_mode < 19

    assert ring_result.classification.confidence >= 0.0
    assert cluster_result.classification.confidence >= 0.0


def test_mode_coefficients_not_all_zero():
    graph = build_canonical_graph()
    engine = VKernelEngine(graph, VKernelConfig(steps=15))

    x = make_ring_input(graph, seed=99)
    result = engine.compute(x)

    assert np.max(np.abs(result.mode_coefficients)) > 0.0


def test_different_inputs_produce_nonidentical_states():
    graph = build_canonical_graph()
    engine = VKernelEngine(graph, VKernelConfig(steps=25))

    x1 = make_radial_input(graph, seed=1)
    x2 = make_cluster_input(graph, seed=2)

    r1 = engine.compute(x1)
    r2 = engine.compute(x2)

    assert not np.allclose(r1.final_state, r2.final_state)
