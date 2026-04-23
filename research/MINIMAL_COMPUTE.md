# Minimal Compute Model

## Core Pipeline

STRUCTURE (G)
→ PROJECTIONS (P)
→ STATE (z₀)
→ DYNAMICS
→ CONVERGENCE
→ MODE (ψₖ)
→ OUTPUT

---

## Core Equation

dz/dt = Lz − βz³

---

## Compute Definition

compute(x) = argmaxₖ ⟨ψₖ, evolve(x)⟩

---

## Interpretation

Computation is not execution.

Computation is convergence to a stable eigenmode.

---

## Minimal Form

Geometry → Interaction → Stability
