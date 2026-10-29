"""Flip operations, as classical analogues only.

In this toy, "quantum flip" is a name for a classical bit operation,
not a claim about quantum mechanics, qubits, or a quantum device:

- bit_flip_all (X-analogue): invert every cell, pattern -> -pattern.
- bit_flip_cells (X-analogue, local): invert exactly the cells in mask.
- phase_flip (Z-analogue, in overlap space): invert the sign of the
  membrane overlap with one stored pattern. It changes a score, never
  a stored pattern, and it is reported as a score operation, not as
  a physical phase.

No superposition, entanglement, or quantum speedup is modelled.
"""

def bit_flip_all(pattern):
    return tuple(-x for x in pattern)

def bit_flip_cells(pattern, mask):
    """Invert cells whose mask entry is True; others unchanged."""
    if len(pattern) != 16 or len(mask) != 16:
        raise ValueError("pattern and mask must each have 16 entries")
    return tuple(-x if m else x for x, m in zip(pattern, mask))

def phase_flip_overlap(overlap):
    """Z-analogue: sign-flip an overlap score."""
    return -overlap
