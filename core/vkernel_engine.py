from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import networkx as nx
import numpy as np


@dataclass
class VKernelConfig:
    steps: int = 40
    alpha_diffusion: float = 0.18
    beta_damping: float = 0.06
    gamma_memory: float = 0.72
    mode_keep: int = 8
    normalize_each_step: bool = True
    epsilon: float = 1e-8


@dataclass
class VKernelResult:
    final_state: np.ndarray
    dominant_mode: int
    dominant_coefficient: float
    mode_coefficients: np.ndarray
    trajectory: np.ndarray
    coefficient_history: np.ndarray
    eigenvalues: np.ndarray
    eigenvectors: np.ndarray


class VKernelEngine:
    """
    Minimal V-Kernel engine.

    Core principle:
        input disturbance -> field evolution -> spectral collapse -> dominant mode
    """

    def __init__(self, graph: nx.Graph, config: Optional[VKernelConfig] = None) -> None:
        if graph.number_of_nodes() == 0:
            raise ValueError("Graph must contain at least one node.")

        self.graph = graph.copy()
        self.config = config or VKernelConfig()

        self.node_order = list(self.graph.nodes())
        self.index_of = {node: i for i, node in enumerate(self.node_order)}

        self.A = nx.to_numpy_array(self.graph, nodelist=self.node_order, weight="weight", dtype=float)
        self.D = np.diag(self.A.sum(axis=1))
        self.L = self.D - self.A

        self.eigenvalues, self.eigenvectors = np.linalg.eigh(self.L)

    def normalize(self, x: np.ndarray) -> np.ndarray:
        denom = np.max(np.abs(x)) + self.config.epsilon
        return x / denom

    def project_to_modes(self, x: np.ndarray, keep: Optional[int] = None) -> np.ndarray:
        keep = keep if keep is not None else self.config.mode_keep
        coeffs = self.eigenvectors.T @ x
        filtered = np.zeros_like(coeffs)
        filtered[:keep] = coeffs[:keep]
        return self.eigenvectors @ filtered

    def mode_coefficients(self, x: np.ndarray) -> np.ndarray:
        return self.eigenvectors.T @ x

    def nonlinear_damping(self, x: np.ndarray) -> np.ndarray:
        return x**3

    def step(self, x: np.ndarray, prev: np.ndarray) -> np.ndarray:
        """
        One evolution step.

        Equation:
            x_{t+1} =
                gamma * x_t
                + alpha * ( -L x_t )
                + projection_to_modes(x_t)
                - beta * x_t^3
                + weak memory(prev)
        """
        cfg = self.config

        diffusion = -(self.L @ x)
        projected = self.project_to_modes(x, keep=cfg.mode_keep)
        damping = self.nonlinear_damping(x)

        new_x = (
            cfg.gamma_memory * x
            + cfg.alpha_diffusion * diffusion
            + 0.18 * projected
            - cfg.beta_damping * damping
            + 0.04 * prev
        )

        if cfg.normalize_each_step:
            new_x = self.normalize(new_x)

        return new_x

    def compute(self, input_signal: np.ndarray) -> VKernelResult:
        """
        Run the V-Kernel computation.

        Args:
            input_signal: array of shape (N,), where N = number of graph nodes

        Returns:
            VKernelResult
        """
        x = np.asarray(input_signal, dtype=float)

        if x.shape != (len(self.node_order),):
            raise ValueError(
                f"input_signal must have shape {(len(self.node_order),)}, got {x.shape}"
            )

        x = self.normalize(x)
        prev = x.copy()

        trajectory: List[np.ndarray] = [x.copy()]
        coefficient_history: List[np.ndarray] = [np.abs(self.mode_coefficients(x))]

        for _ in range(self.config.steps):
            new_x = self.step(x, prev)
            prev = x.copy()
            x = new_x

            trajectory.append(x.copy())
            coefficient_history.append(np.abs(self.mode_coefficients(x)))

        final_coeffs = np.abs(self.mode_coefficients(x))

        if len(final_coeffs) <= 1:
            dominant_mode = 0
        else:
            dominant_mode = int(np.argmax(final_coeffs[1:]) + 1)

        return VKernelResult(
            final_state=x,
            dominant_mode=dominant_mode,
            dominant_coefficient=float(final_coeffs[dominant_mode]),
            mode_coefficients=final_coeffs,
            trajectory=np.array(trajectory),
            coefficient_history=np.array(coefficient_history),
            eigenvalues=self.eigenvalues,
            eigenvectors=self.eigenvectors,
        )


def generate_hex_positions() -> Dict[int, Tuple[float, float]]:
    """
    Canonical 19-node lattice:
    - 1 center
    - 6 first ring
    - 12 second ring
    """
    positions: Dict[int, Tuple[float, float]] = {}
    idx = 0

    positions[idx] = (0.0, 0.0)
    idx += 1

    r1 = 1.0
    for k in range(6):
        angle = 2 * np.pi * k / 6
        positions[idx] = (r1 * np.cos(angle), r1 * np.sin(angle))
        idx += 1

    r2 = 2.0
    for k in range(12):
        angle = 2 * np.pi * k / 12
        positions[idx] = (r2 * np.cos(angle), r2 * np.sin(angle))
        idx += 1

    return positions


def build_canonical_graph(distance_threshold: float = 1.18) -> nx.Graph:
    """
    Build the canonical 19-node V-Kernel lattice.
    """
    pos = generate_hex_positions()
    graph = nx.Graph()

    for node, p in pos.items():
        graph.add_node(node, pos=p)

    nodes = list(graph.nodes())
    for i in nodes:
        xi, yi = graph.nodes[i]["pos"]
        for j in nodes:
            if i >= j:
                continue
            xj, yj = graph.nodes[j]["pos"]
            d = float(np.hypot(xi - xj, yi - yj))
            if d <= distance_threshold:
                graph.add_edge(i, j, weight=1.0)

    return graph


def make_radial_input(graph: nx.Graph, noise: float = 0.2, seed: Optional[int] = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    center = np.array(graph.nodes[0]["pos"], dtype=float)
    x = np.zeros(graph.number_of_nodes(), dtype=float)

    for i in graph.nodes():
        p = np.array(graph.nodes[i]["pos"], dtype=float)
        r = np.linalg.norm(p - center)
        x[i] = np.cos(2.2 * r) + noise * rng.normal()

    return x


def make_ring_input(graph: nx.Graph, noise: float = 0.12, seed: Optional[int] = None) -> np.ndarray:
    rng = np.random.default_rng(seed)
    center = np.array(graph.nodes[0]["pos"], dtype=float)
    x = np.zeros(graph.number_of_nodes(), dtype=float)

    for i in graph.nodes():
        p = np.array(graph.nodes[i]["pos"], dtype=float)
        r = np.linalg.norm(p - center)

        if r < 0.5:
            x[i] = 0.2
        elif r < 1.5:
            x[i] = 1.0
        else:
            x[i] = -0.8

    x += noise * rng.normal(size=x.shape)
    return x


def make_cluster_input(
    graph: nx.Graph,
    hot_nodes: Optional[List[int]] = None,
    cold_nodes: Optional[List[int]] = None,
    noise: float = 0.15,
    seed: Optional[int] = None,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    x = np.zeros(graph.number_of_nodes(), dtype=float)

    hot_nodes = hot_nodes or [2, 4, 8, 11]
    cold_nodes = cold_nodes or [1, 6, 13]

    for i in hot_nodes:
        if i < len(x):
            x[i] = 1.0
    for i in cold_nodes:
        if i < len(x):
            x[i] = -0.8

    x += noise * rng.normal(size=x.shape)
    return x
