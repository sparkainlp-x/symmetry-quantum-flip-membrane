from .membrane import HolographicMembrane, BASE_PATTERNS, SEQUENCE
from .symmetry import OPS, apply_op
from .flip import bit_flip_all, bit_flip_cells
from .gate import RefusingGate, calibrate_tau
from .predictor import PredictiveMembrane
from .demo import main as run_demo
from .full_science import main as run_science

__version__ = "0.1.0"
__all__ = ["HolographicMembrane", "BASE_PATTERNS", "SEQUENCE", "OPS",
           "apply_op", "bit_flip_all", "bit_flip_cells", "RefusingGate",
           "calibrate_tau", "PredictiveMembrane", "run_demo", "run_science",
           "__version__"]
