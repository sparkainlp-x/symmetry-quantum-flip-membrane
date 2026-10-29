"""Deterministic sweeps and probes for the predictive membrane.

All randomness is driven by explicit seeds passed in by callers.
Noise: each cell is bit-flipped independently with probability p.
Junk: uniformly random 16-cell patterns.
A probe is "correct" only when it is accepted AND its predicted
pattern exactly equals the true next pattern (with the same symmetry
transform applied, where applicable).
"""
import random
from .membrane import BASE_PATTERNS, SEQUENCE
from .symmetry import OPS, apply_op
from .flip import bit_flip_all, bit_flip_cells

def noisy(pattern, rng, p):
    return tuple(-x if rng.random() < p else x for x in pattern)

def random_pattern(rng):
    return tuple(rng.choice((-1, 1)) for _ in range(16))

def closed_orbit_patterns():
    out = {}
    for name, pat in BASE_PATTERNS.items():
        for op in OPS:
            out[f"{name}@{op}"] = apply_op(pat, op)
    return out

def run_probe_set(predictive, true_sequence, probes):
    """probes: list of (probe, true_next_pattern). Return counts."""
    accepted = correct = refused = 0
    for probe, true_next in probes:
        r = predictive.recall_and_predict(probe)
        if not r["accepted"]:
            refused += 1
        else:
            accepted += 1
            if r["predicted"] == true_next:
                correct += 1
    return {"n": len(probes), "accepted": accepted,
            "refused": refused, "correct": correct,
            "accuracy_all": correct / len(probes) if probes else 0.0,
            "accuracy_accepted": correct / accepted if accepted else 0.0}

def sweep(predictive_factory, seeds, noise_levels, ops=OPS):
    """Sweep prediction accuracy over noise and symmetry operations.

    predictive_factory: callable returning a fresh PredictiveMembrane
    (already calibrated, frozen gate) for a given storage mode.
    Here the factory is called once per run; the caller supplies it.
    Returns per-(noise, op) accuracy over 40 probes (10 per base pattern).
    """
    results = []
    for p_noise in noise_levels:
        for op in ops:
            total_correct = total_n = 0
            for seed in seeds:
                rng = random.Random(seed)
                probes = []
                for i, base in enumerate(SEQUENCE):
                    true_next_base = SEQUENCE[(i + 1) % len(SEQUENCE)]
                    true_next = apply_op(BASE_PATTERNS[true_next_base], op)
                    for _ in range(10):
                        probe = noisy(apply_op(BASE_PATTERNS[base], op), rng, p_noise)
                        probes.append((probe, true_next))
                # predictive_factory is a no-arg callable in this sweep;
                # it is re-used across seeds because the gate is frozen.
                pred = predictive_factory()
                counts = run_probe_set(pred, SEQUENCE, probes)
                total_correct += counts["correct"]
                total_n += counts["n"]
            results.append({"noise_p": p_noise, "op": op, "n": total_n,
                            "correct": total_correct,
                            "accuracy": total_correct / total_n if total_n else 0.0})
    return results
