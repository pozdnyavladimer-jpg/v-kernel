from core import VKernelAPI, run_vkernel


def test_run_vkernel_with_array():
    result = run_vkernel([0.1] * 19, input_type="array")

    assert result.classification.label != ""
    assert result.engine_result.final_state.shape == (19,)


def test_run_vkernel_with_node_dict():
    signal = {0: 1.0, 4: -0.5, 8: 0.8}
    result = run_vkernel(signal, input_type="node_dict")

    assert result.classification.label != ""
    assert result.engine_result.mode_coefficients.shape[0] == 19


def test_run_vkernel_with_tokens():
    token_map = {
        "flow": [1, 2, 3],
        "cycle": [7, 8, 9, 10],
        "event": [4, 13, 14],
    }

    result = run_vkernel(
        ["flow", "event"],
        input_type="tokens",
        token_map=token_map,
    )

    assert result.classification.label != ""
    assert result.classification.confidence >= 0.0


def test_api_tokens_direct():
    api = VKernelAPI()
    token_map = {
        "flow": [1, 2, 3],
        "cycle": [7, 8, 9, 10],
        "event": [4, 13, 14],
    }

    result = api.run_tokens(["cycle"], token_map=token_map)

    assert result.classification.label != ""
    assert result.engine_result.dominant_mode >= 0
