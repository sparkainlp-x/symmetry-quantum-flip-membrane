"""Holographic membrane: outer-product storage, one-shot projection recall.

Stored patterns are 16-cell tuples in {-1, +1}. The membrane matrix is
the sum of outer products of the stored patterns. Recall is the
projection of a probe onto each stored pattern, reported as a normalised
overlap in [-1, 1]. Overlaps are NOT probabilities and are NOT calibrated
probabilities. This is a classical associative-memory toy, not optical
holography and not a neural or quantum model.
"""

BASE_PATTERNS = {
    # Asymmetric patterns, chosen so each D4 orbit has 8 distinct patterns
    # and no orbit collides with another base pattern's orbit (32 distinct
    # stored patterns in closed-orbit mode). Hand-drawn symmetric patterns
    # (blocks, cross, diag, ring) were REJECTED: blocks is invariant under
    # rot180, ring under several operations, so their orbits collide and
    # recall cannot distinguish which base a transformed probe came from.
    # That collision gave closed-orbit equivariance of only 0.5, measured
    # before this change; it is kept as a falsified design in DESIGN.md.
    "alpha": (-1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1),
    "beta": (1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1),
    "gamma": (1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1),
    "delta": (1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1),
}

SEQUENCE = ("alpha", "beta", "gamma", "delta")

def overlap(a, b):
    if len(a) != 16 or len(b) != 16:
        raise ValueError("patterns must have exactly 16 cells")
    return sum(x * y for x, y in zip(a, b)) / 16.0

class HolographicMembrane:
    """Outer-product memory over named 16-cell patterns."""

    def __init__(self, patterns):
        self.patterns = {}
        for name, pat in patterns.items():
            if len(pat) != 16 or any(x not in (-1, 1) for x in pat):
                raise ValueError(f"pattern {name!r} must be 16 cells in {{-1, +1}}")
            self.patterns[name] = tuple(pat)
        # Outer-product matrix, kept for provenance; recall uses overlaps,
        # which are exactly the normalised projection onto stored patterns.
        self.matrix = [[0.0] * 16 for _ in range(16)]
        for pat in self.patterns.values():
            for i in range(16):
                for j in range(16):
                    self.matrix[i][j] += pat[i] * pat[j]

    def overlaps(self, probe):
        if len(probe) != 16 or any(x not in (-1, 1) for x in probe):
            raise ValueError("probe must be 16 cells in {-1, +1}")
        return {name: overlap(probe, pat) for name, pat in self.patterns.items()}

    def recall(self, probe):
        """Return (best_name, best_overlap, all_overlaps). No gate here."""
        ov = self.overlaps(probe)
        best = max(ov, key=lambda k: ov[k])
        return best, ov[best], ov
