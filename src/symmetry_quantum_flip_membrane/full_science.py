"""Full science run: calibration, sweeps, flips, passport seal.

Run: python -m symmetry_quantum_flip_membrane.full_science
or: symmetry-flip-science (console script, after pip install -e .)
Outputs a JSON payload to stdout (and to --output if given).
"""
import argparse
import json
import random
import sys
from .membrane import BASE_PATTERNS, SEQUENCE, HolographicMembrane
from .symmetry import OPS, apply_op
from .flip import bit_flip_all
from .gate import calibrate_tau, RefusingGate
from .predictor import PredictiveMembrane
from .sweep import noisy, random_pattern, closed_orbit_patterns, run_probe_set, sweep
from .passport import seal

VERSION = "0.1.0"

def build(storage="closed", seed=42):
    rng = random.Random(seed)
    if storage == "closed":
        patterns = closed_orbit_patterns()
    else:
        patterns = dict(BASE_PATTERNS)
    mem = HolographicMembrane(patterns)
    clean = []
    for _ in range(200):
        base = rng.choice(SEQUENCE)
        clean.append(mem.recall(noisy(BASE_PATTERNS[base], rng, 0.05))[1])
    junk = [mem.recall(random_pattern(rng))[1] for _ in range(200)]
    tau, j = calibrate_tau(clean, junk)
    return PredictiveMembrane(mem, RefusingGate(tau)), tau, j

def main(output_path=None):
    closed, tau_closed, j_closed = build("closed")
    base, tau_base, j_base = build("base")
    payload = {"version": VERSION, "seeds": {"calibration": 42, "sweep": [42, 7, 123]},
               "gates": {"closed_orbit": {"tau": tau_closed, "youden_j": j_closed},
                         "base_only": {"tau": tau_base, "youden_j": j_base}}}
    # Closed-orbit sweep: noise x symmetry op
    payload["sweep_closed"] = sweep(lambda: closed, [42, 7, 123], [0.0, 0.05, 0.15, 0.30])
    # Base-only equivariance contrast, clean probes only
    contrast = []
    for op in OPS:
        probes = []
        for i, base_name in enumerate(SEQUENCE):
            true_next = apply_op(BASE_PATTERNS[SEQUENCE[(i + 1) % len(SEQUENCE)]], op)
            probes.append((apply_op(BASE_PATTERNS[base_name], op), true_next))
        contrast.append({"op": op, "closed": run_probe_set(closed, SEQUENCE, probes),
                         "base_only": run_probe_set(base, SEQUENCE, probes)})
    payload["equivariance_contrast_clean"] = contrast
    # Flip tests on the closed-orbit predictive membrane
    rng = random.Random(7)
    flip_results = {}
    flipped = bit_flip_all(BASE_PATTERNS["alpha"])
    r = closed.recall_and_predict(flipped)
    flip_results["bit_flip_all_alpha"] = {"accepted": r["accepted"], "recalled": r["recalled"]}
    junk = [(random_pattern(rng), BASE_PATTERNS["alpha"]) for _ in range(40)]
    flip_results["junk_40"] = run_probe_set(closed, SEQUENCE, junk)
    payload["flip_and_junk"] = flip_results
    payload["headline_allowed"] = False
    payload["headline_note"] = ("No headline claim is emitted. This is a synthetic "
                                "toy only; results apply only to the recorded seeds, "
                                "patterns, and noise levels.")
    payload["passport_seal"] = seal({k: v for k, v in payload.items() if k != "passport_seal"})
    if output_path:
        import pathlib
        p = pathlib.Path(output_path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(payload, indent=2, sort_keys=True))
        return payload
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0

def _cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", default=None)
    args = ap.parse_args()
    result = main(args.output)
    if isinstance(result, dict):
        return 0
    return result

if __name__ == "__main__":
    sys.exit(_cli())
