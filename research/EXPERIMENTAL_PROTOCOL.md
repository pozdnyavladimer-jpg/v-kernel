Experimental Protocol

1. Overview

This document defines an experimental protocol for testing the V-Kernel model.

The purpose is to move from:

- conceptual model
- formal structure
- physical analogy

to:

- measurable behavior
- reproducible experiments
- comparable results

---

2. Experimental Goal

The goal is to test whether the V-Kernel pipeline actually produces:

- coherence growth
- suppression of unstable states
- convergence of candidate fields
- emergence of stable graph structure

---

3. Core Hypothesis

The main hypothesis is:

multiple projections over a shared field,
combined with interaction and pruning,
produce stable attractors more reliably
than single-view or single-state evolution

---

4. System Under Test

The tested system includes:

- canonical graph field
- projection operators
- unified state encoding
- wave / interaction update rule
- candidate field
- convergence metrics

---

5. Experimental Layers

5.1 Base Geometry

Input graph:

- 19-node canonical lattice
- or alternative graph structures for comparison

5.2 Projection Layer

Three projections:

- radial
- ring
- node

5.3 State Layer

State representation:

- real-valued state ("ℝ^6")
- optional complex-valued state ("ℂ^6")

5.4 Interaction Layer

Update rule:

- local neighbor interaction
- weighted propagation
- optional interference model

5.5 Selection Layer

- pruning
- scoring
- convergence detection

---

6. Experimental Conditions

Experiments should be run under multiple conditions.

Condition A — Single State

- one state only
- no candidate field
- basic update rule

Purpose:
baseline comparison

---

Condition B — Multi-Projection, Single Candidate

- 3 projections
- one shared state
- interaction over time

Purpose:
test whether multi-view perception improves stability

---

Condition C — Multi-Projection, Multi-Candidate

- 3 projections
- multiple candidate states
- scoring + selection

Purpose:
test whether candidate competition improves convergence

---

Condition D — Pruning Disabled

- same as C
- pruning removed

Purpose:
measure the role of instability suppression

---

Condition E — Randomized Topology

- same as C
- canonical geometry replaced with random graph

Purpose:
test whether structured geometry matters

---

7. Independent Variables

The following variables may be changed:

- graph topology
- number of candidates
- update strength
- pruning threshold
- phase alignment parameters
- projection weights
- noise level

---

8. Dependent Variables

The following metrics must be recorded:

8.1 Coherence

Measures alignment and global consistency.

8.2 Shadow

Measures dispersion / instability.

8.3 Vitality

Measures dynamic change between time steps.

8.4 Convergence Time

Number of iterations required to reach stable state.

8.5 Candidate Survival Rate

How many candidates remain active over time.

8.6 Final Structural Stability

Persistence of the final attractor after perturbation.

---

9. Core Evaluation Questions

Each experiment should answer:

1. Does coherence increase over time?
2. Does shadow decrease over time?
3. Does the system converge to a stable state?
4. Does pruning improve convergence speed or quality?
5. Does structured geometry outperform random topology?
6. Does multi-candidate evolution outperform single-state evolution?

---

10. Convergence Criterion

A run is considered converged when:

coherence ≥ threshold_c
shadow ≤ threshold_s
vitality ≤ threshold_v

for a sustained number of iterations.

---

11. Perturbation Test

After convergence, apply perturbation:

- random noise
- node deletion
- edge removal
- phase disturbance

Then measure:

- recovery time
- attractor persistence
- candidate regeneration

Purpose:
test resilience of the converged state

---

12. Comparative Baselines

The V-Kernel model should be compared against:

Baseline 1 — Static Graph Diffusion

No projections, no candidate field, no pruning

Baseline 2 — Multi-View Without Selection

Projections exist, but no candidate competition

Baseline 3 — Random Search

Candidates generated randomly, no structured projections

Baseline 4 — Standard Message Passing

Graph update without coherence-based convergence

---

13. Expected Results

If the theory is correct, we expect:

- canonical geometry to converge faster than random topology
- multi-projection models to outperform single-view models
- candidate fields to produce more stable attractors
- pruning to reduce instability and shorten convergence time
- final states to resist perturbation better than baselines

---

14. Visualization Requirements

Each experiment should produce:

- coherence curve
- shadow curve
- vitality curve
- candidate survival curve
- graph evolution snapshots
- final attractor visualization

Optional:

- animated convergence
- interference heatmaps
- phase alignment maps

---

15. Reproducibility Requirements

For every experiment, record:

- random seed
- topology specification
- parameter values
- iteration count
- convergence thresholds
- candidate count
- output metrics

---

16. Minimal Experiment Set

The minimum test suite should include:

1. canonical lattice + single state
2. canonical lattice + multi-projection
3. canonical lattice + candidate field
4. canonical lattice + candidate field + pruning
5. random graph + candidate field + pruning

---

17. Success Criteria

The model is considered experimentally promising if:

- convergence is repeatable
- stable attractors emerge consistently
- structured geometry improves outcomes
- pruning improves robustness
- candidate competition improves final stability

---

18. Research Interpretation

These experiments do not prove a new law of physics.

They test whether the V-Kernel computational principle is valid:

computation = convergence of interacting possibilities

---

19. Next Step After Validation

If experiments support the model, next steps are:

- larger graph scaling
- learned projection operators
- AI-guided candidate generation
- hardware-oriented simplification
- photonic / analog interpretation

---

20. Summary

This protocol transforms V-Kernel from:

- architecture theory
- mathematical model
- physical analogy

into:

- experimental research program
- measurable system
- reproducible computational framework

---

END
