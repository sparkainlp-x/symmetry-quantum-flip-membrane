"""Symmetry operations for a 4x4 pattern, as index permutations.

A pattern is a tuple of 16 values in {-1, +1}, in row-major order.
The dihedral group D4 (8 operations) acts on the grid. These are
classical geometric symmetries only. They are not a claim about
physical, quantum, or biological symmetry.
"""

OPS = ("identity", "rot90", "rot180", "rot270",
       "flip_h", "flip_v", "transpose", "anti_transpose")

def _perm_for(op):
    """Return a tuple p where new[i] = old[p[i]] for grid position i."""
    perm = []
    for r in range(4):
        for c in range(4):
            if op == "identity":
                sr, sc = r, c
            elif op == "rot90":
                sr, sc = 3 - c, r
            elif op == "rot180":
                sr, sc = 3 - r, 3 - c
            elif op == "rot270":
                sr, sc = c, 3 - r
            elif op == "flip_h":
                sr, sc = r, 3 - c
            elif op == "flip_v":
                sr, sc = 3 - r, c
            elif op == "transpose":
                sr, sc = c, r
            elif op == "anti_transpose":
                sr, sc = 3 - c, 3 - r
            else:
                raise ValueError(f"unknown symmetry operation: {op!r}")
            perm.append(sr * 4 + sc)
    return tuple(perm)

PERMS = {op: _perm_for(op) for op in OPS}

INVERSE = {
    "identity": "identity", "rot90": "rot270", "rot180": "rot180",
    "rot270": "rot90", "flip_h": "flip_h", "flip_v": "flip_v",
    "transpose": "transpose", "anti_transpose": "anti_transpose",
}

def apply_op(pattern, op):
    """Apply a D4 operation to a 16-cell pattern."""
    if len(pattern) != 16:
        raise ValueError("pattern must have exactly 16 cells")
    if op not in PERMS:
        raise ValueError(f"unknown symmetry operation: {op!r}")
    perm = PERMS[op]
    return tuple(pattern[perm[i]] for i in range(16))

def inverse_op(op):
    return INVERSE[op]
