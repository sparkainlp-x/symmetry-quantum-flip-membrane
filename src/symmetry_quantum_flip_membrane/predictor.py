"""Predictive membrane: recall, then step forward in a stored sequence.

Prediction in this toy is strictly mechanical: recall the current
pattern with the frozen gate, then predict the next pattern in the
fixed cyclic sequence SEQUENCE. If the recalled pattern is a symmetry
transform of a base pattern (name "base@op" in closed-orbit storage),
the prediction is the same transform of the next base pattern.
"Prediction" here means next-pattern lookup in a toy sequence,
not forecasting a physical, neural, or real-world event.
"""
from .membrane import SEQUENCE, BASE_PATTERNS
from .symmetry import apply_op

NEXT = {name: SEQUENCE[(i + 1) % len(SEQUENCE)] for i, name in enumerate(SEQUENCE)}

def _base_and_op(recalled_name):
    if "@" in recalled_name:
        base, op = recalled_name.split("@", 1)
        return base, op
    return recalled_name, "identity"

class PredictiveMembrane:
    def __init__(self, membrane, gate):
        self.membrane = membrane
        self.gate = gate

    def recall_and_predict(self, probe):
        """Return a dict, or a refusal dict when the gate refuses."""
        name, best, _ = self.membrane.recall(probe)
        if not self.gate.decide(best):
            return {"accepted": False, "recalled": None, "overlap": best,
                    "predicted": None, "predicted_name": None}
        base, op = _base_and_op(name)
        predicted_name = NEXT[base]
        if op == "identity":
            predicted = BASE_PATTERNS[predicted_name]
        else:
            predicted = apply_op(BASE_PATTERNS[predicted_name], op)
        return {"accepted": True, "recalled": name, "overlap": best,
                "predicted": predicted, "predicted_name": predicted_name}
