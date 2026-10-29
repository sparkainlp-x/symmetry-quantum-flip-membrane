"""Demo: symmetry, quantum-flip analogue, predictive membrane.

Run: python -m symmetry_quantum_flip_membrane.demo
or: symmetry-flip-demo (console script, after pip install -e .)
"""
import random
from .membrane import BASE_PATTERNS, SEQUENCE, HolographicMembrane
from .symmetry import OPS, apply_op
from .flip import bit_flip_all, bit_flip_cells
from .gate import calibrate_tau, RefusingGate
from .predictor import PredictiveMembrane
from .sweep import noisy, random_pattern, closed_orbit_patterns, run_probe_set

def build_closed_predictive():
    rng = random.Random(42)
    mem = HolographicMembrane(closed_orbit_patterns())
    clean = []
    for _ in range(200):
        base = rng.choice(SEQUENCE)
        clean.append(mem.recall(noisy(BASE_PATTERNS[base], rng, 0.05))[1])
    junk = [mem.recall(random_pattern(rng))[1] for _ in range(200)]
    tau, j = calibrate_tau(clean, junk)
    return PredictiveMembrane(mem, RefusingGate(tau)), tau, j

def main():
    pred, tau, j = build_closed_predictive()
    print("Symmetry Quantum-Flip Holographic Predictive Membrane - v0.1.0")
    print("Synthetic toy only. Not quantum, not optical holography, not neuroscience.")
    print(f"Frozen gate tau={tau}, calibration Youden J={j}")
    rng = random.Random(7)
    # Clean sequence prediction
    probes = []
    for i, base in enumerate(SEQUENCE):
        true_next = BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]]
        probes.append((BASE_PATTERNS[base], true_next))
    print("clean sequence:", run_probe_set(pred, SEQUENCE, probes))
    # Symmetry equivariance: rotated probes, rotated next patterns
    for op in ("rot90", "flip_h"):
        probes = []
        for i, base in enumerate(SEQUENCE):
            true_next = apply_op(BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]], op)
            probes.append((apply_op(BASE_PATTERNS[base], op), true_next))
        print(f"symmetry {op}:", run_probe_set(pred, SEQUENCE, probes))
    # Quantum-flip analogue: full complement of a stored pattern
    flipped = bit_flip_all(BASE_PATTERNS["alpha"])
    r = pred.recall_and_predict(flipped)
    print("bit_flip_all(alpha) recalled:", r["recalled"], "accepted:", r["accepted"])
    # Single-cell flip, noisy prediction
    mask = [False] * 16
    mask[0] = True
    single = bit_flip_cells(BASE_PATTERNS["beta"], mask)
    r = pred.recall_and_predict(single)
    print("single-cell flip(beta) recalled:", r["recalled"], "accepted:", r["accepted"])
    # Junk refusal
    junk_probes = [(random_pattern(rng), BASE_PATTERNS["alpha"]) for _ in range(40)]
    print("junk 40:", run_probe_set(pred, SEQUENCE, junk_probes))
    # Noisy prediction
    probes = []
    for i, base in enumerate(SEQUENCE):
        true_next = BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]]
        for _ in range(10):
            probes.append((noisy(BASE_PATTERNS[base], rng, 0.15), true_next))
    print("noisy p=0.15, 40 probes:", run_probe_set(pred, SEQUENCE, probes))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
