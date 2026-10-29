import unittest
from symmetry_quantum_flip_membrane.passport import seal, canonical

class TestPassport(unittest.TestCase):
    def test_seal_stable(self):
        obj = {"a": 1, "b": [1, 2]}
        self.assertEqual(seal(obj), seal(obj))
        self.assertEqual(len(seal(obj)), 64)
    def test_seal_changes(self):
        self.assertNotEqual(seal({"a": 1}), seal({"a": 2}))
    def test_canonical_order_independent(self):
        self.assertEqual(canonical({"b": 1, "a": 2}), canonical({"a": 2, "b": 1}))
