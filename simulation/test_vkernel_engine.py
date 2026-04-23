import matplotlib.pyplot as plt
import numpy as np

from core.vkernel_engine import (
    VKernelConfig,
    VKernelEngine,
    build_canonical_graph,
    make_radial_input,
)

graph = build_canonical_graph()

config = VKernelConfig(
    steps=40,
    alpha_diffusion=0.18,
    beta_damping=0.06,
    gamma_memory=0.72,
    mode_keep=8,
)

engine = VKernelEngine(graph, config=config)

x = make_radial_input(graph, seed=42)
result = engine.compute(x)

print("Dominant mode:", result.dominant_mode)
print("Dominant coefficient:", result.dominant_coefficient)

plt.figure(figsize=(10, 4))
for k in range(1, 7):
    plt.plot(result.coefficient_history[:, k], label=f"Mode {k}")
plt.title("Mode Coefficients During Convergence")
plt.xlabel("Step")
plt.ylabel("|coefficient|")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
