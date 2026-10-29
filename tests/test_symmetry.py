import unittest
from symmetry_quantum_flip_membrane.symmetry import OPS, apply_op, inverse_op, PERMS
from symmetry_quantum_flip_membrane.membrane import BASE_PATTERNS

class TestSymmetry(unittest.TestCase):
    def test_ops_are_permutations(self):
        for op in OPS:
            self.assertEqual(sorted(PERMS[op]), list(range(16)))
    def test_identity(self):
        for pat in BASE_PATTERNS.values():
            self.assertEqual(apply_op(pat, "identity"), pat)
    def test_involutions(self):
        for op in ("rot180", "flip_h", "flip_v", "transpose", "anti_transpose"):
            for pat in BASE_PATTERNS.values():
                self.assertEqual(apply_op(apply_op(pat, op), op), pat)
    def test_rot90_four_times(self):
        for pat in BASE_PATTERNS.values():
            p = pat
            for _ in range(4):
                p = apply_op(p, "rot90")
            self.assertEqual(p, pat)
    def test_inverse(self):
        for op in OPS:
            for pat in BASE_PATTERNS.values():
                self.assertEqual(apply_op(apply_op(pat, op), inverse_op(op)), pat)
    def test_bad_op(self):
        with self.assertRaises(ValueError):
            apply_op(BASE_PATTERNS["alpha"], "nope")
    def test_bad_length(self):
        with self.assertRaises(ValueError):
            apply_op((1, -1), "rot90")
