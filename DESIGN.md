# DESIGN — Symmetry Quantum-Flip Holographic Predictive Membrane v0.1.0

## Pipeline

probe (16 cells, +/-1)
  -> membrane overlaps (outer-product projection, normalised overlap)
  -> refusing gate (frozen tau, Youden's J calibration, midpoint of max interval)
  -> if refused: no prediction, no action
  -> if accepted: recalled pattern -> next in cyclic sequence
  -> if recalled pattern is base@op: prediction is next base under the same op

## Storage modes

- closed: 4 base patterns x 8 D4 operations = 32 stored patterns, names base@op.
- base_only: 4 base patterns. Used only as a contrast; it fails equivariance, by design.

## Noise model

Each cell is bit-flipped independently with probability p (0.0, 0.05, 0.15, 0.30 in the sweep). Junk is uniformly random 16-cell patterns. A probe counts as correct only when accepted AND the predicted pattern exactly equals the true next pattern.

## Falsified / negative results kept

- Base-only equivariance fails (measured, not asserted away).
- Noisy prediction degrades with p (measured in the sweep).
- Junk is mostly refused, not always refused; the exact refusal count is reported.
- Bit-flip-all of a stored pattern does not recall that pattern (overlap -1.0); it is reported as refused or as a different recall, never as a success.

## Falsified design kept: symmetric hand patterns

First build used blocks, cross, diag, ring. Measured closed-orbit
equivariance was only 0.5 for rot90, rot270, flip_h, flip_v (4/4 for
identity, rot180, transpose, anti_transpose). Cause: those patterns
are invariant under some D4 operations, so their orbits collide and
recall cannot distinguish which base a transformed probe came from.
Fix: asymmetric alpha/beta/gamma/delta patterns, each orbit 8 distinct,
32 distinct closed-orbit patterns total, no cross-orbit collisions.
Equivariance then measures 4/4 clean for every operation.
