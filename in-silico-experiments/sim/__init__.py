"""In-silico experiment environment for the X-ELRA controller.

This package supplies the experimental environment around the evaluated
controller: the synthetic learner simulator, the evaluation metrics, the
comparator baseline policies, and the configuration loader that parameterises
them. It contains no ARL controller implementation; every governed decision
in the studies and property tests is taken by the deployed X-ELRA governance
code, loaded verbatim by adapters/deployed_policy.py.

Modules
-------
state       : minimal state and mode constants used by the baselines.
dsl         : YAML configuration loader + guarded predicate evaluator.
modes       : the shared perception-to-stance thresholds used by baselines.
baselines   : B1 (direct-ML), B2 (rule-based ITS), B3 (OLM-only),
              B5 (smoothed) comparators.
perception  : synthetic learner simulator with controllable perception noise.
metrics     : oscillation, predictability, audit-sufficiency, fairness metrics.
"""

from .state import ControllerState, MODES, MODE_LABELS
from .dsl import RoutineSet, load_routine_set

__all__ = [
    "ControllerState",
    "MODES",
    "MODE_LABELS",
    "RoutineSet",
    "load_routine_set",
]

__version__ = "2.0.0"
