"""Study 4 -- Concurrency, partial signals, and determinism in practice.

The four published robustness checks, executed against the deployed
governance cycle:

(a) Replay determinism: every decision's pre-decision controller state and
    serialised inputs are persisted (JSON round-trip); an independent policy
    instance re-executes the full cycle from the persisted data alone and
    must reproduce the trace hash, the deterministic item hash, and the
    executed routine.
(b) Order-invariance: shuffling candidate arrival order must not change the
    decision or the deterministic hash over canonically ordered item
    snapshots (the deployed merge sorts by score and identifier before
    selection); the raw persisted inputs record arrival order by design.
(c) Missing-modality guard: on outage streams (feature_gap > 2 mid-stream)
    the deployed controller must route to DIAGNOSTIC and withhold
    pedagogical and affective interventions (P3/P5/P6/P8) on incomplete
    data; the P2 data-integrity probe executing there is the guard working
    and is reported separately. The guard-free counterfactual is the
    harness ablation (the deployed mode inference cannot be de-guarded
    without modifying deployed code).
(d) Late-arriving signal: moving one affect flag from decision i to i+1 must
    change no decision before i (no retroactive mutation) and both runs must
    replay deterministically.
"""

from __future__ import annotations

import copy
import json

import numpy as np

from common import ROUTINES, SEED, save_json
from sim.dsl import load_routine_set
from sim.baselines import B1DirectML
from sim.perception import make_population, make_stream
from deployed_policy import DeployedARLPolicy, fv_from_step, ControllerState

N_POP = 150
N_OI = 60


def _outage_stream(seed, n_steps=40, outage=(15, 31), dt=1.5):
    """A stable NOMINAL learner who suffers a contiguous modality outage.

    During the outage feature_gap>2 (a data source has dropped out) and the
    remaining signals, if taken at face value, read as STRUGGLING (low mastery,
    no recent clicks). A controller that ignores the gap would act on incomplete
    perception; the guarded controller should instead enter DIAGNOSTIC.
    """
    rng = np.random.default_rng(seed)
    stream = []
    for i in range(n_steps):
        t = i * dt
        in_outage = outage[0] <= i < outage[1]
        if in_outage:
            perc = {"lowest_mastery": 0.2, "highest_mastery": 0.5, "mean_mastery": 0.35,
                    "has_mastery": True, "mastery_count": 7, "impressions": 12 + i,
                    "clicks_14d": 0, "days_since_engagement": 1.0, "progress_rate": 0.02,
                    "recent_completions": 0, "active_goals": True,
                    "confusion_flag": False, "frustration_flag": False, "feature_gap": 3,
                    "subgroup": "A"}
        else:
            perc = {"lowest_mastery": 0.6, "highest_mastery": 0.72, "mean_mastery": 0.66,
                    "has_mastery": True, "mastery_count": 7, "impressions": 12 + i,
                    "clicks_14d": 5, "days_since_engagement": 1.0, "progress_rate": 0.02,
                    "recent_completions": 0, "active_goals": True,
                    "confusion_flag": False, "frustration_flag": False, "feature_gap": 0,
                    "subgroup": "A"}
        cands = [{"action_id": f"r{k:03d}", "score": float(rng.random()),
                  "source": "rec", "objective": "pedagogy"} for k in range(10)]
        stream.append((t, perc, cands))
    return stream




PEDAGOGICAL_ROUTINES = {"P3", "P5", "P6", "P8"}


def _persist_run(pol, stream, learner_id="L"):
    """Run the deployed cycle, persisting each decision's pre-cycle state
    (JSON round-trip) and inputs before the decision executes."""
    cs = pol.init_state(stream, learner_id)
    records = []
    for (t, perc, cands) in stream:
        entry_state = json.loads(json.dumps(cs.to_dict(), default=str))
        fv = fv_from_step(perc, cands, t, learner_id)
        rec, cs = pol.decide(cs, fv, learner_id)
        tr = rec["trace"]
        records.append({
            "persisted_state": entry_state,
            "perc": perc, "cands": cands, "t": t,
            "trace_id": tr["trace_id"],
            "deterministic_hash": tr["deterministic_hash"],
            "executed": rec["executed"], "mode": rec["mode"],
        })
    return records


def replay_determinism(pop):
    pol = DeployedARLPolicy(emit_traces=True)
    auditor = DeployedARLPolicy(emit_traces=True)   # independent instance
    total = matches = 0
    for stream in pop:
        for r in _persist_run(pol, stream):
            st = ControllerState.from_dict(r["persisted_state"])
            fv = fv_from_step(r["perc"], r["cands"], r["t"])
            rec2, _ = auditor.decide(st, fv)
            tr2 = rec2["trace"]
            total += 1
            matches += int(tr2["trace_id"] == r["trace_id"]
                           and tr2["deterministic_hash"] == r["deterministic_hash"]
                           and rec2["executed"] == r["executed"])
    return matches, total


def order_invariance(pop, n_shuffles=8, seed=1):
    pol = DeployedARLPolicy(emit_traces=True)
    rng = np.random.default_rng(seed)
    total = dec_inv = hash_inv = 0
    for stream in pop:
        for r in _persist_run(pol, stream):
            ok_dec = ok_hash = True
            for _ in range(n_shuffles):
                shuffled = list(r["cands"])
                rng.shuffle(shuffled)
                st = ControllerState.from_dict(
                    json.loads(json.dumps(r["persisted_state"])))
                fv = fv_from_step(r["perc"], shuffled, r["t"])
                rec_s, _ = pol.decide(st, fv)
                if (rec_s["executed"] != r["executed"]
                        or rec_s["mode"] != r["mode"]):
                    ok_dec = False
                if rec_s["trace"]["deterministic_hash"] != r["deterministic_hash"]:
                    ok_hash = False
                if not (ok_dec or ok_hash):
                    break
            total += 1
            dec_inv += int(ok_dec)
            hash_inv += int(ok_hash)
    return dec_inv, hash_inv, total


def _routine_seq(stream):
    """Executed-routine sequence for one deployed run over a stream."""
    pol = DeployedARLPolicy(emit_traces=True)
    steps = pol.run(stream)
    return [(s.stance, s.trace["decision"]["source_routine"] or "NO_ACTION",
             s.intervened) for s in steps]


def missing_modality_guard(n_learners=120):
    """Deployed guard behaviour on incomplete data, contrasted with the
    ungoverned direct policy B1 (which has no integrity guard) on the same
    streams."""
    rs = load_routine_set(ROUTINES)
    b1 = B1DirectML(rs)

    missing_steps = to_diag = dep_pedagogical = dep_probe = b1_acts = 0
    episodes = ep_dep = ep_b1 = 0
    det_ok = True
    for j in range(n_learners):
        stream = _outage_stream(seed=SEED + 3 + j)
        seq = _routine_seq(stream)
        det_ok = det_ok and (seq == _routine_seq(stream))
        b1_steps = b1.run(stream)
        flag_dep = flag_b1 = False
        for (stance, routine, _), b1s, (t, perc, cands) in zip(seq, b1_steps, stream):
            if perc["feature_gap"] > 2:
                missing_steps += 1
                if stance == "DIAGNOSTIC":
                    to_diag += 1
                if routine in PEDAGOGICAL_ROUTINES:
                    dep_pedagogical += 1
                    flag_dep = True
                if routine == "P2":
                    dep_probe += 1
                if b1s.intervened:
                    b1_acts += 1
                    flag_b1 = True
        episodes += 1
        ep_dep += int(flag_dep)
        ep_b1 += int(flag_b1)
    return {
        "missing_modality_decisions": missing_steps,
        "routed_to_diagnostic_rate": round(to_diag / max(missing_steps, 1), 4),
        "deployed_pedagogical_action_rate":
            round(dep_pedagogical / max(missing_steps, 1), 4),
        "deployed_integrity_probe_rate":
            round(dep_probe / max(missing_steps, 1), 4),
        "unguarded_b1_action_rate":
            round(b1_acts / max(missing_steps, 1), 4),
        "episodes": episodes,
        "episodes_deployed_pedagogical_on_incomplete_data": ep_dep,
        "episodes_unguarded_b1_acted": ep_b1,
        "determinism_on_outage_streams": bool(det_ok),
        "note": "P2 is the data-integrity probe permitted in DIAGNOSTIC (the "
                "guard acting); pedagogical/affective routines are P3/P5/P6/P8. "
                "The unguarded contrast is the direct policy B1, which has no "
                "integrity guard and acts on the incomplete perception.",
    }


def late_signal_snapshot(seed=11):
    stream = make_stream(seed=seed, archetype="boundary_affect", sigma=0.12, n_steps=80)
    idx = None
    # Prefer a mid-stream boundary so the no-retroactivity check is
    # non-trivial (decisions 0..idx-1 must be unchanged).
    for lo in (10, 0):
        for i in range(lo, len(stream) - 1):
            if stream[i][1]["confusion_flag"] and not stream[i + 1][1]["confusion_flag"]:
                idx = i
                break
        if idx is not None:
            break
    if idx is None:
        return {"applicable": False}
    late = copy.deepcopy(stream)
    late[idx][1]["confusion_flag"] = False
    late[idx + 1][1]["confusion_flag"] = True

    def run(stream_):
        steps = DeployedARLPolicy().run(stream_)
        return [(s.stance, s.intervened, s.action) for s in steps]

    base = run(stream)
    late_r = run(late)
    differing = [i for i, (a, b) in enumerate(zip(base, late_r)) if a != b]
    det = (run(stream) == base) and (run(late) == late_r)
    n = len(base)
    return {
        "applicable": True, "shift_index": idx,
        "n_decisions": n,
        "n_differing_decisions": len(differing),
        "first_differing_index": (min(differing) if differing else None),
        "last_differing_index": (max(differing) if differing else None),
        "no_retroactive_change": bool(not differing or min(differing) >= idx),
        "reconverged_before_end": bool(differing and max(differing) < n - 1),
        "both_runs_deterministic": bool(det),
    }


def main():
    pop = make_population(seed=SEED, n_learners=N_POP, sigma=0.15, n_steps=80,
                          archetype_weights={"boundary_mastery": 0.5,
                                             "boundary_affect": 0.5})
    print("=== Study 4 (deployed): (a) replay determinism ===")
    rd_match, rd_total = replay_determinism(pop)
    print(f"  {rd_match}/{rd_total}")
    print("=== (b) order invariance ===")
    oi_dec, oi_hash, oi_total = order_invariance(pop[:N_OI])
    print(f"  decision {oi_dec}/{oi_total}, canonical hash {oi_hash}/{oi_total}")
    print("=== (c) missing-modality guard ===")
    guard = missing_modality_guard()
    print("=== (d) late signal ===")
    late = late_signal_snapshot()

    out = {
        "study": "study4_robustness",
        "system": "deployed governance modules (ARL_dep)",
        "replay_determinism": {"matches": rd_match, "total": rd_total,
                               "rate": round(rd_match / max(rd_total, 1), 6),
                               "method": "persist pre-decision state + inputs "
                                         "(JSON round-trip); independent instance "
                                         "re-executes the full cycle"},
        "order_invariance": {
            "decision_invariant": oi_dec, "canonical_hash_invariant": oi_hash,
            "total": oi_total,
            "decision_rate": round(oi_dec / max(oi_total, 1), 6),
            "hash_rate": round(oi_hash / max(oi_total, 1), 6)},
        "missing_modality_guard": guard,
        "late_signal_snapshot": late,
    }
    save_json("study4_robustness.json", out)

    print(f"\n(a) Replay determinism: {rd_match}/{rd_total} "
          f"({100*rd_match/max(rd_total,1):.2f}%)")
    print(f"(b) Order-invariance: decision {oi_dec}/{oi_total}, "
          f"canonical hash {oi_hash}/{oi_total}")
    g = guard
    print(f"(c) Guard: {g['missing_modality_decisions']} incomplete-data decisions, "
          f"{100*g['routed_to_diagnostic_rate']:.0f}% to DIAGNOSTIC; pedagogical "
          f"actions {100*g['deployed_pedagogical_action_rate']:.0f}% (integrity probe "
          f"{100*g['deployed_integrity_probe_rate']:.0f}%) vs ungoverned B1 "
          f"{100*g['unguarded_b1_action_rate']:.0f}%; episodes "
          f"{g['episodes_deployed_pedagogical_on_incomplete_data']}/{g['episodes']} vs "
          f"{g['episodes_unguarded_b1_acted']}/{g['episodes']}; "
          f"determinism={g['determinism_on_outage_streams']}")
    print(f"(d) Late signal: {late.get('n_differing_decisions')} differing from index "
          f"{late.get('first_differing_index')} (shift at {late.get('shift_index')}); "
          f"no_retroactive_change={late.get('no_retroactive_change')}, "
          f"deterministic={late.get('both_runs_deterministic')}")
    return out


if __name__ == "__main__":
    main()
