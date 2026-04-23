from __future__ import annotations

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from core.api import VKernelAPI


def smooth_field(pos: dict, values: np.ndarray, sigma: float = 0.40, size: int = 250):
    xs = np.array([pos[i][0] for i in pos])
    ys = np.array([pos[i][1] for i in pos])

    gx = np.linspace(xs.min() - 0.7, xs.max() + 0.7, size)
    gy = np.linspace(ys.min() - 0.7, ys.max() + 0.7, size)
    XX, YY = np.meshgrid(gx, gy)

    ZZ = np.zeros_like(XX, dtype=float)
    for x0, y0, v in zip(xs, ys, values):
        ZZ += v * np.exp(-((XX - x0) ** 2 + (YY - y0) ** 2) / (2 * sigma**2))

    return XX, YY, ZZ, xs, ys


def plot_result(graph: nx.Graph, title: str, state: np.ndarray, mode_coeffs: np.ndarray) -> None:
    pos = nx.get_node_attributes(graph, "pos")
    XX, YY, ZZ, xs, ys = smooth_field(pos, state)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # field
    ax = axes[0]
    ax.contourf(XX, YY, ZZ, levels=60, cmap="seismic", alpha=0.92)
    ax.contour(XX, YY, ZZ, levels=[0], colors="white", linewidths=1.6)
    nx.draw_networkx_edges(graph, pos, ax=ax, edge_color="white", alpha=0.16)
    ax.scatter(xs, ys, c="black", s=16)
    ax.set_title(title)
    ax.axis("equal")
    ax.axis("off")

    # coefficients
    ax = axes[1]
    ax.bar(range(min(10, len(mode_coeffs))), mode_coeffs[:10])
    ax.set_title("Mode coefficients")
    ax.set_xlabel("Mode index")
    ax.set_ylabel("|coefficient|")
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


def main():
    api = VKernelAPI()
    graph = api.graph

    print("=== V-KERNEL RESONANCE AI DEMO ===")

    cases = [
        ("Radial Input", api.run_radial(noise=0.08, seed=42)),
        ("Ring Input", api.run_ring(noise=0.08, seed=43)),
        (
            "Cluster Input",
            api.run_cluster(
                hot_nodes=[2, 4, 8, 11],
                cold_nodes=[1, 6, 13],
                noise=0.05,
                seed=44,
            ),
        ),
    ]

    for name, result in cases:
        print()
        print(f"[{name}]")
        print(result.summary())
        print("Description:", result.classification.description)

        plot_result(
            graph=graph,
            title=f"{name} -> {result.classification.label}",
            state=result.engine_result.final_state,
            mode_coeffs=result.engine_result.mode_coefficients,
        )

    print()
    print("=== DEMO COMPLETE ===")


if __name__ == "__main__":
    main()
