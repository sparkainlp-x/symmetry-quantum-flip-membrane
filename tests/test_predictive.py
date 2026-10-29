import unittest
import random
from symmetry_quantum_flip_membrane.membrane import BASE_PATTERNS, SEQUENCE, HolographicMembrane
from symmetry_quantum_flip_membrane.symmetry import apply_op
from symmetry_quantum_flip_membrane.gate import calibrate_tau, RefusingGate
from symmetry_quantum_flip_membrane.predictor import PredictiveMembrane
from symmetry_quantum_flip_membrane.sweep import noisy, random_pattern, closed_orbit_patterns, run_probe_set

def build(storage="closed", seed=42):
    rng = random.Random(seed)
    patterns = closed_orbit_patterns() if storage == "closed" else dict(BASE_PATTERNS)
    mem = HolographicMembrane(patterns)
    clean = [mem.recall(noisy(BASE_PATTERNS[rng.choice(SEQUENCE)], rng, 0.05))[1] for _ in range(200)]
    junk = [mem.recall(random_pattern(rng))[1] for _ in range(200)]
    tau, j = calibrate_tau(clean, junk)
    return PredictiveMembrane(mem, RefusingGate(tau)), tau, j

class TestPredictive(unittest.TestCase):
    def test_clean_sequence_prediction_closed(self):
        pred, _, _ = build("closed")
        probes = []
        for i, base in enumerate(SEQUENCE):
            probes.append((BASE_PATTERNS[base], BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]]))
        counts = run_probe_set(pred, SEQUENCE, probes)
        self.assertEqual(counts["correct"], 4)
        self.assertEqual(counts["accepted"], 4)
    def test_closed_equivariance_rot90(self):
        pred, _, _ = build("closed")
        probes = []
        for i, base in enumerate(SEQUENCE):
            probes.append((apply_op(BASE_PATTERNS[base], "rot90"),
                           apply_op(BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]], "rot90")))
        counts = run_probe_set(pred, SEQUENCE, probes)
        self.assertEqual(counts["correct"], 4)
    def test_base_only_equivariance_is_worse(self):
        closed, _, _ = build("closed")
        base, _, _ = build("base")
        for op in ("rot90", "flip_h"):
            probes = []
            for i, b in enumerate(SEQUENCE):
                probes.append((apply_op(BASE_PATTERNS[b], op),
                               apply_op(BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]], op)))
            c = run_probe_set(closed, SEQUENCE, probes)["correct"]
            bcount = run_probe_set(base, SEQUENCE, probes)["correct"]
            self.assertEqual(c, 4)
            self.assertLess(bcount, 4)
    def test_junk_mostly_refused(self):
        pred, tau, _ = build("closed")
        self.assertGreater(tau, 0.3)
        rng = random.Random(7)
        probes = [(random_pattern(rng), BASE_PATTERNS["alpha"]) for _ in range(40)]
        counts = run_probe_set(pred, SEQUENCE, probes)
        self.assertGreaterEqual(counts["refused"], 30)
    def test_gate_frozen(self):
        _, tau, _ = build("closed")
        gate = RefusingGate(tau)
        self.assertTrue(gate.decide(1.0))
        self.assertFalse(gate.decide(0.0))
    def test_noisy_prediction_degrades(self):
        pred, _, _ = build("closed")
        rng = random.Random(7)
        clean = []
        noisy_probes = []
        for i, base in enumerate(SEQUENCE):
            nxt = BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]]
            clean.append((BASE_PATTERNS[base], nxt))
            for _ in range(10):
                noisy_probes.append((noisy(BASE_PATTERNS[base], rng, 0.30), nxt))
        c = run_probe_set(pred, SEQUENCE, clean)["accuracy_all"]
        n = run_probe_set(pred, SEQUENCE, noisy_probes)["accuracy_all"]
        self.assertEqual(c, 1.0)
        self.assertLess(n, 1.0)
