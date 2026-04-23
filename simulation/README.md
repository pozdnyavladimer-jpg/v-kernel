V-Kernel Simulations

This folder contains executable simulations and notebooks for the V-Kernel research model.

The simulations demonstrate how a fixed graph geometry can support:

- candidate field generation
- interaction and pruning
- convergence to stable states
- graph eigenmodes
- petal-like structures
- resonance-based classification

---

Start Here

If you are new to the project, use this order:

1. "vkernel_full_research_demo.ipynb"
   → full walkthrough of the research pipeline

2. "vkernel_resonance_ai.ipynb"
   → resonance-based classification prototype

3. "demo_resonance_ai.py"
   → minimal runnable Python demo (no notebook required)

---

Simulation Index

"vkernel_full_research_demo.ipynb"

Complete research walkthrough:

- canonical 19-node lattice
- radial / ring / node projections
- candidate field generation
- live convergence
- Laplacian eigenmodes
- petal-mode emergence
- Bindu interpretation

Best entry point for understanding the whole system.

---

"vkernel_resonance_ai.ipynb"

Prototype of resonance-based AI:

input → disturbance → field evolution → dominant mode → output

Demonstrates:

- input as field perturbation
- interaction-driven stabilization
- mode selection as classification

---

"vkernel_petal_modes.ipynb"

Explains how petal-like structures emerge from graph eigenmodes.

Focus:

- Laplacian
- spectral modes
- smooth field rendering
- symmetry and stable patterns

Best notebook for understanding why “petals” appear.

---

"vkernel_mode_to_candidate_bridge.ipynb"

Connects:

- candidate field dynamics
- spectral mode decomposition

Shows how noisy candidate states collapse toward stable allowed modes.

---

"vkernel_live_simulation.ipynb"

Dynamic candidate-field simulation with:

- noise
- wave-like update
- pruning
- convergence metrics
- Bindu emergence

Useful for observing stabilization over time.

---

"demo_resonance_ai.py"

Minimal executable script.

Runs several inputs through the resonance pipeline and prints:

- dominant mode
- label
- confidence

Useful for quick tests outside notebooks.

---

Conceptual Pipeline

All simulations are variations of the same research model:

geometry → projections → candidate field → interaction → pruning → convergence → mode

Interpretation:

- geometry defines constraints
- projections define perception
- candidate field defines possible states
- interaction drives evolution
- pruning removes instability
- convergence selects a stable mode

---

Main Parameters

Most notebooks expose a small set of tunable parameters.

"SEED"

Controls reproducibility.

- same seed → same initialization
- different seed → different trajectories

---

"NUM_CANDIDATES"

Controls how many candidate states compete.

Higher values:

- more exploration
- slower runtime
- richer competition

Suggested range:

5 – 20

---

"STEPS"

Controls convergence time.

Higher values:

- more time to stabilize
- better late-stage observation

Suggested range:

20 – 60

---

"NOISE_LEVEL"

Controls how chaotic the initial candidate field is.

Higher values:

- more exploration
- less stability

Lower values:

- smoother convergence
- less diversity

Suggested range:

0.05 – 0.30

---

"PRUNE_THRESHOLD"

Controls when weak amplitudes are removed.

Higher values:

- aggressive cleanup
- faster simplification
- risk of over-pruning

Lower values:

- more survival
- more retained noise

Suggested range:

0.05 – 0.20

---

"sigma" in "smooth_field(...)"

Controls only the rendering.

Higher values:

- smoother, more blended fields

Lower values:

- sharper local structure
- stronger boundaries

Suggested range:

0.30 – 0.55

---

How to Tune Behavior

Stronger convergence

Use:

- lower noise
- moderate pruning
- fewer candidates

Example:

NOISE_LEVEL = 0.10
PRUNE_THRESHOLD = 0.12
NUM_CANDIDATES = 8

---

More exploration

Use:

- higher noise
- lower pruning
- more candidates

Example:

NOISE_LEVEL = 0.25
PRUNE_THRESHOLD = 0.06
NUM_CANDIDATES = 15

---

Cleaner petal shapes

Use:

- lower noise
- lower-order mode selection
- slightly larger rendering sigma

---

Sharper petal boundaries

Use:

- smaller sigma
- stronger contour display
- less smoothing

---

How to Read the Outputs

Canonical lattice

The base graph geometry.

This defines what interactions are allowed.

---

Candidate field

A noisy or structured initial state.

This is not yet the result.

It is the space of possibilities.

---

Convergence curves

Coherence
Rising coherence means stronger global alignment.

Shadow
Lower shadow means less dispersion / inconsistency.

Vitality
Lower vitality means the field is stabilizing.

Active candidates
Fewer active candidates means pruning is working.

---

Petal modes

These are stable graph eigenmodes.

They are not drawn manually.

They emerge from the geometry of the lattice.

---

Mode coefficients

These show how strongly a state overlaps with each graph mode.

A strong dominant coefficient indicates collapse toward one stable mode.

---

Best Practices

Change one parameter at a time

Do not tune everything at once.

Good order:

1. noise
2. pruning
3. candidate count
4. graph geometry

---

Keep the seed fixed during comparisons

This makes differences meaningful.

---

Record interesting runs

When you see useful behavior, record:

- seed
- candidates
- steps
- noise
- pruning threshold
- any mode settings

---

Suggested Experiments

1. Noise sensitivity

Try:

0.05 / 0.10 / 0.20 / 0.30

Question:
How much noise can the system tolerate?

---

2. Pruning sensitivity

Try:

0.03 / 0.08 / 0.12 / 0.18

Question:
When does pruning become too weak or too aggressive?

---

3. Candidate competition

Try:

5 / 10 / 15 / 20 candidates

Question:
Does stronger competition improve stability?

---

4. Geometry comparison

Replace the canonical graph with:

- random graph
- grid graph
- larger flower lattice

Question:
How strongly do stable modes depend on geometry?

---

What These Simulations Are

These simulations are:

- research demonstrations
- parameter exploration tools
- figure generators
- executable prototypes

---

What These Simulations Are Not

They are not yet:

- production compute engines
- hardware implementations
- proofs of quantum physics
- general-purpose optimizers

They are research prototypes for field-based graph computation.

---

Minimal Takeaway

The graph defines possible interactions.
The field explores candidate states.
Interaction and pruning remove instability.
What survives is a stable mode allowed by the geometry.

That is the core V-Kernel simulation idea.

---
