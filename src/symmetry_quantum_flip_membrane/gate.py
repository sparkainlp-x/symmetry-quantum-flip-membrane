"""Refusing gate, calibrated once and then frozen.

Calibration scans tau in [0, 1] on labelled calibration probes
(clean stored-pattern probes vs random junk probes) and picks the
midpoint of the interval of tau values achieving maximal Youden's J
(sensitivity + specificity - 1). After calibration, tau is frozen:
it is never re-tuned on held-out probes. A probe is accepted only if
its best membrane overlap is >= tau; otherwise the membrane refuses,
and no action is taken. Refusal is a property of this toy, not a
safety guarantee for any real system.
"""

def calibrate_tau(clean_overlaps, junk_overlaps):
    """Return (tau, best_j). Overlaps are best-overlap scores."""
    best_j = -2.0
    best_taus = []
    tau = 0.0
    while tau <= 1.0001:
        tp = sum(1 for x in clean_overlaps if x >= tau)
        fn = len(clean_overlaps) - tp
        tn = sum(1 for x in junk_overlaps if x < tau)
        fp = len(junk_overlaps) - tn
        sens = tp / len(clean_overlaps) if clean_overlaps else 0.0
        spec = tn / len(junk_overlaps) if junk_overlaps else 0.0
        j = sens + spec - 1.0
        if j > best_j + 1e-12:
            best_j = j
            best_taus = [tau]
        elif abs(j - best_j) <= 1e-12:
            best_taus.append(tau)
        tau = round(tau + 0.01, 10)
    tau_mid = (best_taus[0] + best_taus[-1]) / 2.0
    return round(tau_mid, 4), round(best_j, 4)

class RefusingGate:
    def __init__(self, tau):
        self.tau = tau

    def decide(self, best_overlap):
        """Return True (accept) iff best_overlap >= frozen tau."""
        return best_overlap >= self.tau
