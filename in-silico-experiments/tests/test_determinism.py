"""Property-based determinism tests of the deployed X-ELRA controller.

Run: python3 tests/test_determinism.py

Exercises the DEPLOYED governance code (loaded verbatim via the experiment
adapter, production routine configuration) over randomly generated controller
states and perception inputs, and checks three properties per case:

  1. Determinism: the same state and inputs produce the identical decision,
     routine path, and successor state.
  2. Replay: a decision re-executed from the serialised (JSON round-tripped)
     controller state reproduces the decision and successor state exactly.
  3. Candidate-order invariance: permuting the arrival order of candidate
     actions changes neither the decision nor the canonical item hash (the
     raw inputs record arrival order by design).

The only runtime substitution is the clock read by the deployed
windowed-oscillation check (pinned to the decision timestamp, restoring the
production coincidence of wall time and decision time). No deployed logic is
modified.
"""

from __future__ import annotations

import copy
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "adapters"))

from deployed_policy import DeployedARLPolicy, fv_from_step, T0  # noqa: E402

import dxelra.arl.boundedness as _db  # noqa: E402
from dxelra.arl.controller_state import ControllerState  # noqa: E402

_SIM_NOW = [T0]


class _PinnedClock:
    @staticmethod
    def now(tz=None):
        return _SIM_NOW[0]


_db.datetime = _PinnedClock

N_CASES = 3000
SEED = 20260601


def rand_perc(rng):
    has_mastery = rng.random() > 0.1
    return {
        "lowest_mastery": float(rng.random()) if has_mastery else 0.0,
        "highest_mastery": float(0.5 + 0.5 * rng.random()) if has_mastery else 0.0,
        "mean_mastery": float(rng.random()) if has_mastery else 0.0,
        "has_mastery": has_mastery,
        "mastery_count": int(rng.integers(0, 8)),
        "impressions": int(rng.integers(0, 40)),
        "clicks_14d": int(rng.integers(0, 10)),
        "days_since_engagement": float(rng.random() * 25.0),
        "progress_rate": float(rng.random() * 0.1),
        "recent_completions": int(rng.integers(0, 3)),
        "active_goals": bool(rng.random() > 0.3),
        "confusion_flag": bool(rng.random() > 0.9),
        "frustration_flag": bool(rng.random() > 0.9),
        "feature_gap": int(rng.integers(0, 5)),
    }


def rand_cands(rng):
    n = int(rng.integers(1, 8))
    return [{"action_id": f"c{int(rng.integers(0, 999)):03d}_{i}",
             "score": float(np.round(rng.random(), 6)),
             "source": "a", "objective": "pedagogy"} for i in range(n)]


def decide_at(policy, cs, perc, cands, t):
    fv = fv_from_step(perc, cands, t)
    _SIM_NOW[0] = fv.generated_at
    return policy.decide(copy.deepcopy(cs), fv)


def rec_sig(rec):
    return (rec["mode"], rec["executed"], rec["action"], rec["mode_transition"],
            tuple((p["routine_name"], p["outcome"]) for p in rec["path"]))


def main():
    rng = np.random.default_rng(SEED)
    policy = DeployedARLPolicy(emit_traces=False)
    tpolicy = DeployedARLPolicy(emit_traces=True)

    n_det = n_replay = n_order = 0
    for case in range(N_CASES):
        # random reachable state: walk a random prefix from init
        t = 0.0
        cs = policy.init_state([(t, rand_perc(rng), rand_cands(rng))])
        for _ in range(int(rng.integers(0, 12))):
            t += float(1.0 + rng.random() * 7.0)
            _, cs = decide_at(policy, cs, rand_perc(rng), rand_cands(rng), t)

        t += float(1.0 + rng.random() * 7.0)
        perc, cands = rand_perc(rng), rand_cands(rng)

        # 1. determinism: identical twice
        r1, s1 = decide_at(policy, cs, perc, cands, t)
        r2, s2 = decide_at(policy, cs, perc, cands, t)
        assert rec_sig(r1) == rec_sig(r2), f"case {case}: nondeterministic record"
        assert s1.to_dict() == s2.to_dict(), f"case {case}: nondeterministic state"
        n_det += 1

        # 2. replay from serialised state (JSON round trip)
        cs_rt = ControllerState.from_dict(json.loads(json.dumps(cs.to_dict())))
        r3, s3 = decide_at(policy, cs_rt, perc, cands, t)
        assert rec_sig(r3) == rec_sig(r1), f"case {case}: replay diverged"
        assert s3.to_dict() == s1.to_dict(), f"case {case}: replay state diverged"
        n_replay += 1

        # 3. candidate-order invariance (decision + canonical hash)
        if case % 3 == 0:
            perm = list(cands)
            rng.shuffle(perm)
            ta, _ = decide_at(tpolicy, cs, perc, cands, t)
            tb, _ = decide_at(tpolicy, cs, perc, perm, t)
            assert rec_sig(ta)[:4] == rec_sig(tb)[:4], \
                f"case {case}: decision changed under candidate permutation"
            assert (ta["trace"]["deterministic_hash"]
                    == tb["trace"]["deterministic_hash"]), \
                f"case {case}: canonical hash changed under candidate permutation"
            n_order += 1

    print(f"PASS test_determinism: {N_CASES} random cases on the deployed "
          f"controller; determinism ({n_det}) + replay ({n_replay}) + "
          f"order-invariance ({n_order}) all hold.")


if __name__ == "__main__":
    main()
