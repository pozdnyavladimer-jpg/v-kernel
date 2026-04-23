from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Optional, Sequence

import networkx as nx
import numpy as np


@dataclass
class EncoderConfig:
    normalize_output: bool = True
    epsilon: float = 1e-8


class DisturbanceEncoder:
    """
    Input -> graph disturbance encoder.

    Converts external data into a node-aligned field vector z0
    that can be passed into VKernelEngine.compute(...).

    Supported sources:
    - scalar per node
    - node dictionary
    - text-like tokens
    - edge emphasis
    - simple templates (radial / ring / cluster)
    """

    def __init__(self, graph: nx.Graph, config: Optional[EncoderConfig] = None) -> None:
        if graph.number_of_nodes() == 0:
            raise ValueError("Graph must contain at least one node.")

        self.graph = graph
        self.config = config or EncoderConfig()
        self.node_order = list(graph.nodes())
        self.node_index = {node: i for i, node in enumerate(self.node_order)}

    def _normalize(self, x: np.ndarray) -> np.ndarray:
        if not self.config.normalize_output:
            return x
        denom = np.max(np.abs(x)) + self.config.epsilon
        return x / denom

    def zeros(self) -> np.ndarray:
        return np.zeros(len(self.node_order), dtype=float)

    def from_array(self, values: Sequence[float]) -> np.ndarray:
        x = np.asarray(values, dtype=float)
        expected = (len(self.node_order),)
        if x.shape != expected:
            raise ValueError(f"Expected shape {expected}, got {x.shape}")
        return self._normalize(x)

    def from_node_dict(self, values: Mapping[int, float], default: float = 0.0) -> np.ndarray:
        x = np.full(len(self.node_order), default, dtype=float)
        for node, value in values.items():
            if node not in self.node_index:
                continue
            x[self.node_index[node]] = float(value)
        return self._normalize(x)

    def from_active_nodes(
        self,
        hot_nodes: Optional[Iterable[int]] = None,
        cold_nodes: Optional[Iterable[int]] = None,
        hot_value: float = 1.0,
        cold_value: float = -0.8,
    ) -> np.ndarray:
        x = self.zeros()

        for node in hot_nodes or []:
            if node in self.node_index:
                x[self.node_index[node]] = hot_value

        for node in cold_nodes or []:
            if node in self.node_index:
                x[self.node_index[node]] = cold_value

        return self._normalize(x)

    def radial_template(self, frequency: float = 2.2, center_node: int = 0) -> np.ndarray:
        if center_node not in self.graph.nodes:
            raise ValueError(f"Center node {center_node} not found in graph.")

        center = np.array(self.graph.nodes[center_node]["pos"], dtype=float)
        x = self.zeros()

        for node in self.graph.nodes():
            p = np.array(self.graph.nodes[node]["pos"], dtype=float)
            r = np.linalg.norm(p - center)
            x[self.node_index[node]] = np.cos(frequency * r)

        return self._normalize(x)

    def ring_template(
        self,
        center_threshold: float = 0.5,
        inner_threshold: float = 1.5,
        center_value: float = 0.2,
        inner_value: float = 1.0,
        outer_value: float = -0.8,
        center_node: int = 0,
    ) -> np.ndarray:
        if center_node not in self.graph.nodes:
            raise ValueError(f"Center node {center_node} not found in graph.")

        center = np.array(self.graph.nodes[center_node]["pos"], dtype=float)
        x = self.zeros()

        for node in self.graph.nodes():
            p = np.array(self.graph.nodes[node]["pos"], dtype=float)
            r = np.linalg.norm(p - center)

            if r < center_threshold:
                x[self.node_index[node]] = center_value
            elif r < inner_threshold:
                x[self.node_index[node]] = inner_value
            else:
                x[self.node_index[node]] = outer_value

        return self._normalize(x)

    def cluster_template(
        self,
        hot_nodes: Optional[List[int]] = None,
        cold_nodes: Optional[List[int]] = None,
    ) -> np.ndarray:
        hot_nodes = hot_nodes or [2, 4, 8, 11]
        cold_nodes = cold_nodes or [1, 6, 13]
        return self.from_active_nodes(hot_nodes=hot_nodes, cold_nodes=cold_nodes)

    def from_edge_emphasis(
        self,
        active_edges: Sequence[tuple[int, int]],
        edge_value: float = 1.0,
        spread_to_neighbors: bool = True,
        neighbor_value: float = 0.35,
    ) -> np.ndarray:
        x = self.zeros()

        for u, v in active_edges:
            if u in self.node_index:
                x[self.node_index[u]] += edge_value
            if v in self.node_index:
                x[self.node_index[v]] += edge_value

            if spread_to_neighbors:
                for node in (u, v):
                    if node not in self.graph:
                        continue
                    for nbr in self.graph.neighbors(node):
                        x[self.node_index[nbr]] += neighbor_value

        return self._normalize(x)

    def from_text_tokens(
        self,
        tokens: Sequence[str],
        token_map: Optional[Dict[str, List[int]]] = None,
        default_weight: float = 1.0,
    ) -> np.ndarray:
        """
        Simple symbolic encoder:
        maps tokens to groups of graph nodes.

        Example token_map:
        {
            "flow": [1,2,3],
            "cycle": [7,8,9,10,11,12],
            "event": [4,13,14]
        }
        """
        token_map = token_map or {}
        x = self.zeros()

        for token in tokens:
            nodes = token_map.get(token, [])
            for node in nodes:
                if node in self.node_index:
                    x[self.node_index[node]] += default_weight

        return self._normalize(x)

    def add_noise(self, x: np.ndarray, scale: float = 0.1, seed: Optional[int] = None) -> np.ndarray:
        rng = np.random.default_rng(seed)
        y = np.asarray(x, dtype=float).copy()
        y += scale * rng.normal(size=y.shape)
        return self._normalize(y)

    def blend(self, *signals: np.ndarray, weights: Optional[Sequence[float]] = None) -> np.ndarray:
        if not signals:
            raise ValueError("At least one signal is required.")

        arrs = [np.asarray(s, dtype=float) for s in signals]
        for i, arr in enumerate(arrs):
            if arr.shape != (len(self.node_order),):
                raise ValueError(f"Signal {i} has invalid shape {arr.shape}")

        if weights is None:
            weights = [1.0] * len(arrs)

        if len(weights) != len(arrs):
            raise ValueError("weights length must match number of signals")

        out = np.zeros(len(self.node_order), dtype=float)
        for arr, w in zip(arrs, weights):
            out += float(w) * arr

        return self._normalize(out)
