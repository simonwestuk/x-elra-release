"""Generate genuine sample decision records from the deployed controller.

Runs the deployed X-ELRA governance code (loaded verbatim via the experiment
adapter, production routine configuration) on crafted scenarios and persists
the resulting decision records:
  - sample_trace_struggling.json : affective-overload intervention (P8 executes)
  - sample_trace_noaction.json   : deliberate non-intervention (fall-through,
    all eligible routines blocked or skipped, recorded with reasons)
"""

from __future__ import annotations

import copy
import json
import os
import sys
from datetime import timedelta

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "adapters"))

from common import SAMPLE_DIR
from deployed_policy import DeployedARLPolicy, fv_from_step, T0


def main():
    pol = DeployedARLPolicy(emit_traces=True)

    cands = [{"action_id": f"py101_res_{k:02d}", "score": round(0.9 - 0.05 * k, 3),
              "source": "hybrid_recommender", "objective": "pedagogy"}
             for k in range(10)]

    # Scenario 1: affective overload -> STRUGGLING -> P8 executes.
    perc = {"lowest_mastery": 0.1, "highest_mastery": 0.85, "mean_mastery": 0.45,
            "has_mastery": True, "mastery_count": 7, "impressions": 40,
            "clicks_14d": 4, "days_since_engagement": 0.5, "progress_rate": 0.02,
            "recent_completions": 0, "active_goals": True,
            "confusion_flag": True, "frustration_flag": True, "feature_gap": 0}
    cs = pol.init_state([(0.0, perc, cands)], learner_id="std_demo_0001")
    cs.budgets.interventions_remaining = 4
    cs.budgets.suggestions_remaining = 8
    cs.timers.mark_execution("P6", now=T0 + timedelta(minutes=25))
    fv = fv_from_step(perc, cands, 30.0, learner_id="std_demo_0001")
    rec, cs_after = pol.decide(copy.deepcopy(cs), fv, learner_id="std_demo_0001")
    with open(os.path.join(SAMPLE_DIR, "sample_trace_struggling.json"), "w") as fh:
        json.dump(rec["trace"], fh, indent=2)

    # Scenario 2: same stance, but the intervention budget is exhausted and the
    # eligible routines are blocked -> deliberate non-intervention fall-through;
    # the record still carries the full evaluation path with reasons.
    cs2 = copy.deepcopy(cs)
    cs2.budgets.interventions_remaining = 0
    cs2.budgets.suggestions_remaining = 0
    cs2.timers.mark_execution("P3", now=T0 + timedelta(minutes=29))
    cs2.timers.mark_execution("P8", now=T0 + timedelta(minutes=29))
    fv2 = fv_from_step(perc, cands, 30.0, learner_id="std_demo_0002")
    rec2, _ = pol.decide(copy.deepcopy(cs2), fv2, learner_id="std_demo_0002")
    with open(os.path.join(SAMPLE_DIR, "sample_trace_noaction.json"), "w") as fh:
        json.dump(rec2["trace"], fh, indent=2)

    print("Sample traces written to", SAMPLE_DIR)
    print("  scenario 1 decision:", rec["action"], "via", rec["executed"],
          "| trace_id", rec["trace"]["trace_id"][:16])
    print("  scenario 2 decision:", rec2["action"] or "NO_ACTION", "via",
          rec2["executed"], "(intervened=%s)" % rec2["intervened"],
          "| trace_id", rec2["trace"]["trace_id"][:16])
    print("  scenario 2 routine path:",
          [(o["routine_name"], o["outcome"], o["reason"]) for o in rec2["path"]])


if __name__ == "__main__":
    main()
