# V-Kernel Simulation

This folder contains dynamic simulations of the V-Kernel architecture.

## v_kernel_field_visual.ipynb

Visual representation of:

- field evolution
- noise injection
- pruning (entropy reduction)
- coherence stabilization

This is not a neural network.

This is a dynamic field system.


---

## demo.ipynb

Minimal V-Kernel demonstration.

Shows:

- noise-driven field evolution
- propagation through weighted graph
- reinforcement and decay
- entropy pruning
- emergence of bindu
- coherence stabilization

This demo is the simplest visible proof of the V-Kernel execution model.

---

V-Kernel Full Research Demo — Guide

What this notebook does

This notebook is a research demonstration of the V-Kernel idea:

geometry -> projections -> candidate field -> convergence -> petal modes -> bindu

It shows how a fixed graph geometry can support:

- multiple projections of the same structure
- noisy candidate fields
- interaction and pruning
- convergence to a stable configuration
- decomposition into graph eigenmodes
- emergence of petal-like stable patterns

This notebook is not a hardware implementation.
It is a field computation prototype and research visualization tool.

---

Conceptual pipeline

The notebook follows this sequence:

1. Structure

A canonical 19-node lattice is created.

This is the base geometric field.

2. Projections

Three projections read different aspects of the same field:

- radial
- ring
- node

These produce different measurements from the same graph state.

3. Candidate field

A noisy initial field is created over the lattice.

This represents a superposition of possible states.

4. Live convergence

Multiple candidates evolve through:

- local interaction
- wave-like update
- pruning
- scoring

The strongest candidate survives.

5. Spectral decomposition

The graph Laplacian is computed.

Its eigenmodes define the allowed stable field patterns of the lattice.

6. Petal mode interpretation

Low-order eigenmodes appear as symmetric lobes / petals.

These are not drawn manually.
They emerge from the geometry.

7. Bindu

The dominant local point of the converged state is interpreted as Bindu:

- attractor anchor
- strongest local state
- stable reference point

---

Main sections of the notebook

Section A — Canonical lattice

Builds and displays the 19-node graph.

Section B — Projections

Defines:

- "radial_projection"
- "ring_projection"
- "node_projection"

Section C — State and metrics

Defines:

- encoded state
- coherence
- shadow
- vitality
- scoring

Section D — Candidate dynamics

Runs noisy candidate evolution and pruning.

Section E — Laplacian modes

Computes graph eigenmodes and visualizes petal-like patterns.

Section F — Bridge

Shows how live convergence relates to stable graph modes.

---

Parameters you can change

The notebook is designed so behavior can be changed mainly through configuration values.

Random seed

SEED = 42

Controls reproducibility.

- same seed -> same random initialization
- different seed -> different candidate fields

Use this when testing repeatability.

---

Number of candidates

NUM_CANDIDATES = 10

Controls how many candidate states compete.

Higher values:

- more exploration
- slower runtime
- richer competition

Lower values:

- simpler behavior
- faster runtime
- weaker selection pressure

Suggested range:

- 5 to 20

---

Number of steps

STEPS = 25

Controls how long convergence is allowed to run.

Higher values:

- more time to stabilize
- better for observing late convergence

Lower values:

- faster runs
- useful for quick testing

Suggested range:

- 20 to 60

---

Noise level

NOISE_LEVEL = 0.18

Controls how chaotic the candidate field is during evolution.

Higher values:

- more entropy
- more exploration
- harder convergence

Lower values:

- smoother dynamics
- easier convergence
- less diversity

Suggested range:

- 0.05 to 0.30

---

Prune threshold

PRUNE_THRESHOLD = 0.10

Controls when weak amplitudes are removed.

Higher values:

- aggressive pruning
- faster simplification
- risk of killing useful structure

Lower values:

- more candidate survival
- slower cleanup
- more noise retained

Suggested range:

- 0.05 to 0.20

---

Metric weights

ALPHA_COHERENCE = 1.0
BETA_SHADOW = 0.8
GAMMA_VITALITY = 0.6

These define the score:

score = coherence - shadow - vitality

Interpretation:

- "ALPHA_COHERENCE"
  rewards global alignment

- "BETA_SHADOW"
  penalizes inconsistency / dispersion

- "GAMMA_VITALITY"
  penalizes rapid change

If convergence is too unstable:

- increase "BETA_SHADOW"
- increase "GAMMA_VITALITY"

If exploration dies too early:

- reduce pruning
- reduce "GAMMA_VITALITY"

---

Functions you can customize

"build_graph()"

Defines the lattice itself.

Change this if you want:

- a larger flower lattice
- random graph comparison
- grid / hex / scale-free topology

This is the main place to test whether geometry matters.

---

"radial_projection()"

Captures flow and gradient relative to the center.

Change this if you want:

- stronger center bias
- distance-weighted flow
- directional asymmetry

---

"ring_projection()"

Captures cyclic / radial organization.

Change this if you want:

- more rings
- smoother radial bins
- stronger resonance weighting

---

"node_projection()"

Captures node-local structure.

Currently it depends on amplitude and degree.

Change this if you want:

- clustering coefficient
- centrality
- local motif weighting

---

"encode_state()"

Maps raw projections into the compact state vector.

This is where you define what the system “measures”.

You can change:

- the number of components
- the meaning of components
- the normalization method

This is one of the most important experimentation points.

---

"wave_update()"

Defines how local interaction spreads through the graph.

This is the main dynamics function.

Change this if you want:

- stronger mixing
- weaker memory
- oscillatory behavior
- more damping

---

"prune()"

Defines when weak states disappear.

This controls entropy reduction.

---

"smooth_field()"

Controls how node values are rendered as continuous fields.

It does not change the graph dynamics itself.
It changes only the visualization.

Main parameter:

sigma=0.40

Higher sigma:

- smoother, more blended fields
- more “wave” appearance

Lower sigma:

- sharper, more localized lobes
- more node-like appearance

Suggested range:

- 0.30 to 0.55

---

How to tune behavior

If you want stronger convergence

Use:

- lower "NOISE_LEVEL"
- moderate "PRUNE_THRESHOLD"
- higher "ALPHA_COHERENCE"
- lower "NUM_CANDIDATES"

Example:

NOISE_LEVEL = 0.10
PRUNE_THRESHOLD = 0.12
ALPHA_COHERENCE = 1.2

---

If you want more exploration

Use:

- higher "NOISE_LEVEL"
- lower "PRUNE_THRESHOLD"
- more candidates

Example:

NUM_CANDIDATES = 15
NOISE_LEVEL = 0.25
PRUNE_THRESHOLD = 0.06

---

If you want cleaner petal shapes

Use:

- lower noise
- stronger mode filtering
- slightly larger rendering sigma

Example:

- reduce noise in candidate generation
- use lower-order dominant modes
- set "sigma=0.45"

---

If you want sharper petal boundaries

Use:

- smaller "sigma"
- stronger contour lines
- lower smoothing

Example:

sigma=0.32

---

What the outputs mean

Canonical lattice figure

Shows the base structure.

This is the geometry that constrains all later behavior.

---

Candidate field figure

Shows the noisy initial field.

This is not yet a stable result.
It is a superposition / candidate state.

---

Convergence metric plots

Coherence

If this rises, the system is becoming more globally aligned.

Shadow

If this falls, the system is becoming less inconsistent.

Vitality

If this falls, the system is stabilizing.

Active candidates

If this falls, pruning and competition are working.

---

Live converged candidate

Shows the strongest candidate after interaction.

This is the system’s selected dynamic result.

---

Petal modes

Show stable graph eigenmodes.

These are the allowed modal structures of the lattice.

They explain why the geometry tends to produce recurring symmetric field patterns.

---

Mode coefficient plot

Shows how strongly the final candidate overlaps with each graph mode.

A strong dominant mode means the converged field is close to one of the lattice’s natural stable structures.

---

How to experiment safely

Best practice:

Change only one thing at a time

For example:

- first only noise
- then only pruning
- then only candidate count

Do not change everything at once.

---

Keep the seed fixed when comparing

Use the same "SEED" while tuning one parameter.

That makes differences meaningful.

---

Record settings

When you get an interesting result, record:

- seed
- candidate count
- steps
- noise
- pruning threshold
- metric weights

---

Suggested experiments

Experiment 1 — Noise sensitivity

Try:

NOISE_LEVEL = 0.05, 0.10, 0.20, 0.30

Question:
How much noise can the system tolerate before convergence breaks?

---

Experiment 2 — Pruning sensitivity

Try:

PRUNE_THRESHOLD = 0.03, 0.08, 0.12, 0.18

Question:
When does pruning become too weak or too aggressive?

---

Experiment 3 — Candidate competition

Try:

NUM_CANDIDATES = 5, 10, 15, 20

Question:
Does stronger competition improve stability?

---

Experiment 4 — Geometry comparison

Replace "build_graph()" with:

- random graph
- grid graph
- larger lattice

Question:
Do petal-like stable modes depend on geometry?

---

What this notebook is for

This notebook is useful for:

- conceptual demonstration
- research explanation
- parameter tuning
- candidate-to-mode interpretation
- generating figures for README / paper / posts

---

What this notebook is not

This notebook is not yet:

- a production compute engine
- a hardware design
- a proof of quantum physics
- a universal optimizer

It is a research prototype for field-based graph computation.

---

Minimal takeaway

The main idea demonstrated here is:

The graph defines possible interactions.
The field explores candidate states.
Interaction and pruning remove unstable structure.
What survives is a stable mode allowed by the geometry.

That is the core V-Kernel intuition.

---

END
