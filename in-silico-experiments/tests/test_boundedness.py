"""Property tests for boundedness of the deployed X-ELRA controller.

Run: python3 tests/test_boundedness.py

Runs the DEPLOYED governance code (loaded verbatim via the experiment adapter,
production routine configuration) over randomly generated perception streams
and verifies, at every decision of every stream:

  - Safety (budgets): interventions_remaining and suggestions_remaining stay
    within [0, capacity] at every reachable state.
  - Safety (windowed interventions): bounded interventions within any sliding
    oscillation window (30 min) never exceed the intervention capacity.
  - Cooldown: no routine executes twice within its configured cooldown.
  - Stability (dwell spacing): consecutive stance changes are separated by at
    least the 300-second dwell, which bounds stance changes per window.

The only runtime substitution is the clock read by the deployed
windowed-oscillation check (pinned to the decision timestamp). No deployed
logic is modified.
"""

from __future__ import annotations

import copy
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "adapters"))

from deployed_policy import DeployedARLPolicy, fv_from_step, T0  # noqa: E402

import dxelra.arl.boundedness as _db  # noqa: E402
from dxelra.arl.boundedness import _get_cooldown  # noqa: E402
from dxelra.arl.controller_state import ControllerBudgets  # noqa: E402

_SIM_NOW = [T0]


class _PinnedClock:
    @staticmethod
    def now(tz=None):
        return _SIM_NOW[0]


_db.datetime = _PinnedClock

N_STREAMS = 960
N_STEPS = 80
STEP_MIN = 1.5
WINDOW_MIN = 30.0
DWELL_S = 300.0
SEED = 20260601


def stream_perc(rng, regime, k):
    """Perception at step k for a random regime (drifting + noisy)."""
    drift = regime["mastery0"] + regime["trend"] * k + rng.normal(0, regime["noise"])
    low = float(np.clip(drift, 0.0, 1.0))
    return {
        "lowest_mastery": low,
        "highest_mastery": float(np.clip(low + 0.3, 0.0, 1.0)),
        "mean_mastery": float(np.clip(low + 0.15, 0.0, 1.0)),
        "has_mastery": True,
        "mastery_count": 7,
        "impressions": 12 + k,
        "clicks_14d": int(rng.integers(0, 2)) if low < 0.4 else int(rng.integers(2, 8)),
        "days_since_engagement": regime["days_lapsed"] if rng.random() < 0.05 else 1.0,
        "progress_rate": float(np.clip(rng.normal(regime["rate"], 0.01), 0, 0.2)),
        "recent_completions": int(rng.integers(0, 2)),
        "active_goals": True,
        "confusion_flag": bool(rng.random() < regime["affect_p"]),
        "frustration_flag": bool(rng.random() < regime["affect_p"]),
        "feature_gap": 3 if rng.random() < 0.05 else 0,
    }


CANDS = [{"action_id": f"c{i}", "score": (i % 5) / 5.0, "source": "a",
          "objective": "pedagogy"} for i in range(4)]


def main():
    rng = np.random.default_rng(SEED)
    fresh = ControllerBudgets()
    cap_i, cap_s = fresh.interventions_remaining, fresh.suggestions_remaining

    policy = DeployedARLPolicy(emit_traces=False)
    cooldowns = {r.name: _get_cooldown(r) for r in policy.bundle.routines}

    max_iv_window = 0
    max_changes_window = 0
    min_change_gap_s = float("inf")
    cooldown_violations = 0

    for s_i in range(N_STREAMS):
        regime = {
            "mastery0": float(rng.random()),
            "trend": float(rng.normal(0, 0.01)),
            "noise": float(0.02 + rng.random() * 0.2),
            "rate": float(rng.random() * 0.08),
            "affect_p": float(rng.random() * 0.15),
            "days_lapsed": float(16 + rng.random() * 10),
        }
        t = 0.0
        cs = policy.init_state([(t, stream_perc(rng, regime, 0), CANDS)])
        iv_times, change_times = [], []
        exec_times = {}
        prev_mode = cs.mode

        for k in range(N_STEPS):
            t = k * STEP_MIN
            fv = fv_from_step(stream_perc(rng, regime, k), CANDS, t)
            _SIM_NOW[0] = fv.generated_at
            rec, cs = policy.decide(copy.deepcopy(cs), fv)

            # budgets in range at every reachable state
            assert 0 <= cs.budgets.interventions_remaining <= cap_i, \
                f"stream {s_i} step {k}: interventions budget out of range"
            assert 0 <= cs.budgets.suggestions_remaining <= cap_s, \
                f"stream {s_i} step {k}: suggestions budget out of range"

            if rec["intervened"]:
                iv_times.append(t)
            if cs.mode != prev_mode:
                if change_times:
                    gap = (t - change_times[-1]) * 60.0
                    min_change_gap_s = min(min_change_gap_s, gap)
                change_times.append(t)
                prev_mode = cs.mode

            # cooldown: executed routine respects its configured cooldown
            if rec["executed"] != "NO_ACTION":
                rn = rec["executed"]
                cd = cooldowns.get(rn, 0)
                if rn in exec_times and cd:
                    assert (t - exec_times[rn]) * 60.0 >= cd, \
                        f"stream {s_i} step {k}: {rn} executed within cooldown"
                exec_times[rn] = t

        for times, tracker in ((iv_times, "iv"), (change_times, "ch")):
            for i, ti in enumerate(times):
                in_win = sum(1 for tj in times if ti - WINDOW_MIN < tj <= ti)
                if tracker == "iv":
                    assert in_win <= cap_i, \
                        f"stream {s_i}: {in_win} interventions in one window"
                    max_iv_window = max(max_iv_window, in_win)
                else:
                    max_changes_window = max(max_changes_window, in_win)

    if min_change_gap_s < float("inf"):
        assert min_change_gap_s >= DWELL_S, \
            f"stance changes {min_change_gap_s:.0f}s apart (dwell {DWELL_S:.0f}s)"

    gap_txt = ("no stream produced two stance changes"
               if min_change_gap_s == float("inf")
               else f"min stance-change spacing = {min_change_gap_s:.0f}s "
                    f"(dwell {DWELL_S:.0f}s)")
    print(f"PASS test_boundedness: {N_STREAMS} streams on the deployed "
          f"controller. max interventions/window = {max_iv_window} "
          f"(capacity {cap_i}); max stance changes/window = "
          f"{max_changes_window}; {gap_txt}; cooldowns respected.")


if __name__ == "__main__":
    main()
