import unittest
from symmetry_quantum_flip_membrane.membrane import HolographicMembrane, BASE_PATTERNS, overlap
from symmetry_quantum_flip_membrane.flip import bit_flip_all, bit_flip_cells, phase_flip_overlap

class TestMembraneFlip(unittest.TestCase):
    def setUp(self):
        self.mem = HolographicMembrane(BASE_PATTERNS)
    def test_clean_recall(self):
        for name, pat in BASE_PATTERNS.items():
            best, ov, _ = self.mem.recall(pat)
            self.assertEqual(best, name)
            self.assertEqual(ov, 1.0)
    def test_overlap_range(self):
        for pat in BASE_PATTERNS.values():
            for ov in self.mem.overlaps(pat).values():
                self.assertGreaterEqual(ov, -1.0)
                self.assertLessEqual(ov, 1.0)
    def test_bit_flip_all_involutive(self):
        for pat in BASE_PATTERNS.values():
            self.assertEqual(bit_flip_all(bit_flip_all(pat)), pat)
            self.assertEqual(overlap(bit_flip_all(pat), pat), -1.0)
    def test_single_cell_flip_overlap(self):
        pat = BASE_PATTERNS["alpha"]
        mask = [False] * 16
        mask[0] = True
        flipped = bit_flip_cells(pat, mask)
        self.assertEqual(overlap(flipped, pat), 0.875)
    def test_phase_flip(self):
        self.assertEqual(phase_flip_overlap(0.5), -0.5)
    def test_bad_pattern(self):
        with self.assertRaises(ValueError):
            HolographicMembrane({"bad": (1, -1)})
