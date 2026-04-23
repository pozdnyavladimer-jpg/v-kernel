from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Union

import networkx as nx
import numpy as np

from core.io_encoders import DisturbanceEncoder, EncoderConfig
from core.mode_classifier import ClassificationResult, ModeClassifier
from core.vkernel_engine import (
    VKernelConfig,
    VKernelEngine,
    VKernelResult,
    build_canonical_graph,
)


InputLike = Union[
    np.ndarray,
    Sequence[float],
    Dict[int, float],
    List[str],
]


@dataclass
class VKernelAPIResult:
    input_signal: np.ndarray
    engine_result: VKernelResult
    classification: ClassificationResult

    def summary(self) -> str:
        c = self.classification
        return (
            f"Mode {c.dominant_mode} -> {c.label} | "
            f"confidence={c.confidence:.3f} | "
            f"coefficient={c.dominant_coefficient:.3f}"
        )


class VKernelAPI:
    """
    High-level API for V-Kernel.

    Full pipeline:
        raw input -> disturbance encoding -> field evolution -> mode classification
    """

    def __init__(
        self,
        graph: Optional[nx.Graph] = None,
        engine_config: Optional[VKernelConfig] = None,
        encoder_config: Optional[EncoderConfig] = None,
        classifier: Optional[ModeClassifier] = None,
    ) -> None:
        self.graph = graph or build_canonical_graph()
        self.encoder = DisturbanceEncoder(self.graph, config=encoder_config)
        self.engine = VKernelEngine(self.graph, config=engine_config)
        self.classifier = classifier or ModeClassifier()

    # --------------------------------------------------
    # Low-level run
    # --------------------------------------------------
    def run_signal(self, signal: np.ndarray) -> VKernelAPIResult:
        x = np.asarray(signal, dtype=float)
        engine_result = self.engine.compute(x)
        classification = self.classifier.classify_result(engine_result)

        return VKernelAPIResult(
            input_signal=x,
            engine_result=engine_result,
            classification=classification,
        )

    # --------------------------------------------------
    # Encoded input helpers
    # --------------------------------------------------
    def run_array(self, values: Sequence[float]) -> VKernelAPIResult:
        x = self.encoder.from_array(values)
        return self.run_signal(x)

    def run_node_dict(self, values: Dict[int, float], default: float = 0.0) -> VKernelAPIResult:
        x = self.encoder.from_node_dict(values, default=default)
        return self.run_signal(x)

    def run_tokens(
        self,
        tokens: Sequence[str],
        token_map: Optional[Dict[str, List[int]]] = None,
        default_weight: float = 1.0,
    ) -> VKernelAPIResult:
        x = self.encoder.from_text_tokens(
            tokens=tokens,
            token_map=token_map,
            default_weight=default_weight,
        )
        return self.run_signal(x)

    def run_active_nodes(
        self,
        hot_nodes: Optional[Sequence[int]] = None,
        cold_nodes: Optional[Sequence[int]] = None,
        hot_value: float = 1.0,
        cold_value: float = -0.8,
    ) -> VKernelAPIResult:
        x = self.encoder.from_active_nodes(
            hot_nodes=hot_nodes,
            cold_nodes=cold_nodes,
            hot_value=hot_value,
            cold_value=cold_value,
        )
        return self.run_signal(x)

    # --------------------------------------------------
    # Template inputs
    # --------------------------------------------------
    def run_radial(
        self,
        frequency: float = 2.2,
        center_node: int = 0,
        noise: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> VKernelAPIResult:
        x = self.encoder.radial_template(frequency=frequency, center_node=center_node)
        if noise is not None and noise > 0:
            x = self.encoder.add_noise(x, scale=noise, seed=seed)
        return self.run_signal(x)

    def run_ring(
        self,
        center_threshold: float = 0.5,
        inner_threshold: float = 1.5,
        center_value: float = 0.2,
        inner_value: float = 1.0,
        outer_value: float = -0.8,
        center_node: int = 0,
        noise: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> VKernelAPIResult:
        x = self.encoder.ring_template(
            center_threshold=center_threshold,
            inner_threshold=inner_threshold,
            center_value=center_value,
            inner_value=inner_value,
            outer_value=outer_value,
            center_node=center_node,
        )
        if noise is not None and noise > 0:
            x = self.encoder.add_noise(x, scale=noise, seed=seed)
        return self.run_signal(x)

    def run_cluster(
        self,
        hot_nodes: Optional[List[int]] = None,
        cold_nodes: Optional[List[int]] = None,
        noise: Optional[float] = None,
        seed: Optional[int] = None,
    ) -> VKernelAPIResult:
        x = self.encoder.cluster_template(
            hot_nodes=hot_nodes,
            cold_nodes=cold_nodes,
        )
        if noise is not None and noise > 0:
            x = self.encoder.add_noise(x, scale=noise, seed=seed)
        return self.run_signal(x)

    def run_edges(
        self,
        active_edges: Sequence[tuple[int, int]],
        edge_value: float = 1.0,
        spread_to_neighbors: bool = True,
        neighbor_value: float = 0.35,
    ) -> VKernelAPIResult:
        x = self.encoder.from_edge_emphasis(
            active_edges=active_edges,
            edge_value=edge_value,
            spread_to_neighbors=spread_to_neighbors,
            neighbor_value=neighbor_value,
        )
        return self.run_signal(x)

    def run_blended(
        self,
        signals: Sequence[np.ndarray],
        weights: Optional[Sequence[float]] = None,
    ) -> VKernelAPIResult:
        x = self.encoder.blend(*signals, weights=weights)
        return self.run_signal(x)


# ------------------------------------------------------
# Convenience function
# ------------------------------------------------------
def run_vkernel(
    input_data: InputLike,
    *,
    input_type: str = "array",
    graph: Optional[nx.Graph] = None,
    engine_config: Optional[VKernelConfig] = None,
    encoder_config: Optional[EncoderConfig] = None,
    classifier: Optional[ModeClassifier] = None,
    token_map: Optional[Dict[str, List[int]]] = None,
) -> VKernelAPIResult:
    """
    Convenience wrapper.

    Examples:
        run_vkernel([0.1, 0.2, ...], input_type="array")
        run_vkernel({0: 1.0, 4: -0.3}, input_type="node_dict")
        run_vkernel(["flow", "event"], input_type="tokens", token_map=...)
    """
    api = VKernelAPI(
        graph=graph,
        engine_config=engine_config,
        encoder_config=encoder_config,
        classifier=classifier,
    )

    if input_type == "array":
        return api.run_array(input_data)  # type: ignore[arg-type]

    if input_type == "node_dict":
        return api.run_node_dict(input_data)  # type: ignore[arg-type]

    if input_type == "tokens":
        return api.run_tokens(input_data, token_map=token_map)  # type: ignore[arg-type]

    raise ValueError(
        f"Unsupported input_type={input_type!r}. "
        f"Use one of: 'array', 'node_dict', 'tokens'."
      )
