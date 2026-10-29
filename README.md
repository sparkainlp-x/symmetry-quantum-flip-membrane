# Symmetry Quantum-Flip Holographic Predictive Membrane — v0.1.0

A standard-library-only synthetic toy, in the same format as world-projection v0.3.0: an installable package, frozen refusing gate, deterministic sweeps, and a SHA-256 evidence passport.

## What it is

- **Holographic membrane:** outer-product storage of four asymmetric 16-cell (4x4) patterns (alpha, beta, gamma, delta), one-shot projection recall by normalised overlap. Overlaps are NOT probabilities.
- **Symmetry:** the dihedral group D4 (identity, rot90, rot180, rot270, flip_h, flip_v, transpose, anti_transpose) acting on the 4x4 grid.
- **Quantum flip, as a classical analogue only:** bit_flip_all (invert every cell, X-analogue) and bit_flip_cells (invert chosen cells), plus phase_flip_overlap (sign-flip an overlap score). No superposition, entanglement, qubit, or quantum speedup is modelled, and no quantum claim is made.
- **Predictive membrane:** recall the current pattern with the frozen gate, then predict the next pattern in the fixed cyclic sequence alpha -> beta -> gamma -> delta -> alpha. If the recalled pattern is a symmetry transform, the prediction is the same transform of the next pattern.

## Key contrast, built in

- **Closed-orbit storage** (base patterns + all 8 D4 transforms, 32 stored patterns) is equivariant by construction: a transformed probe recalls its transformed pattern and predicts its transformed next pattern.
- **Base-only storage** (4 patterns) is NOT equivariant: transformed probes are recalled as the wrong base pattern or refused. The package measures this contrast, it does not hide it.

## Install and run

```sh
pip install -e .
python -m unittest discover -s tests
symmetry-flip-demo
symmetry-flip-science
```

## Honest limits

- Synthetic toy only. NOT quantum mechanics, NOT optical holography, NOT neuroscience, NOT a brain, NOT a forecast of any real event, NOT a safety system.
- Results apply only to the recorded seeds, patterns, noise levels, and symmetry operations.
- The gate is calibrated once (Youden's J, midpoint of the maximal interval) and then frozen; it is never re-tuned on held-out probes.
- No headline claim is emitted. See `full_science.py`: `headline_allowed` is always False.

## Licence and credits

AGPL-3.0-only. Project author: Jean-Francois Brisson only. Mun Seok Lee is cited as inspiration only, not as co-author, because this package contains no Digital to Wave, Coherent Sequence, C_seq, or OES-32 code.
