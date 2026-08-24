"""Study 5 -- Runtime cost/latency and fairness parity.

Latency: per-decision wall time of the deployed governance cycle (mode
inference + bounded routine evaluation + state transition) and, separately,
with full decision-record emission (trace build + serialisation), as a
function of candidate-set size and routine-set size. Routine-set inflation
uses inert cold_start-gated padding in a temporary YAML copy, mirroring the
published harness method; deployed/ files are never modified. The deployed
service adds transport/persistence overhead measured separately in the live
deployment (Chapter 6); this study isolates the governance core, matching the
harness study's scope.

Fairness: subgroup intervention-density parity, deployed vs harness ARL and
the unbounded direct-ML baseline, on the published subgroup populations.
"""
from common import ROUTINES, SEED, save_json
from sim.dsl import load_routine_set
import copy
import json as _json
import time

import numpy as np

from sim.baselines import B1DirectML
from sim.perception import make_population, make_stream
from sim import metrics as M
from deployed_policy import (DeployedARLPolicy, fv_from_step,
                             make_padded_bundle_path)

REPS = 400
N_PER_GROUP = 150


def _steady_state(pol, warm_steps=12):
    stream = make_stream(seed=1, archetype="boundary_affect", sigma=0.12,
                         n_steps=warm_steps)
    cs = pol.init_state(stream)
    for (t, perc, cands) in stream:
        _, cs = pol.decide(cs, fv_from_step(perc, cands, t))
    _, perc, _ = stream[-1]
    return cs, perc


def time_decide(pol, cs0, perc, cands, reps=REPS):
    fv = fv_from_step(perc, cands, 100.0)
    states = [copy.deepcopy(cs0) for _ in range(reps + 50)]
    for i in range(50):                       # warmup
        pol.decide(states[i], fv)
    t0 = time.perf_counter()
    for i in range(50, 50 + reps):
        pol.decide(states[i], fv)
    return (time.perf_counter() - t0) / reps * 1e6


def latency_table():
    core = DeployedARLPolicy(emit_traces=False)
    traced = DeployedARLPolicy(emit_traces=True)
    cs0, perc = _steady_state(core)

    by_candidates = []
    for c in [1, 5, 10, 25, 50, 100, 250, 500]:
        cands = [{"action_id": f"r{k:04d}",
                  "score": float((k * 2654435761 % 1000) / 1000.0),
                  "source": "agent", "objective": "pedagogy"} for k in range(c)]
        us_core = time_decide(core, cs0, perc, cands)
        us_traced = time_decide(traced, cs0, perc, cands)
        rec, _ = traced.decide(copy.deepcopy(cs0), fv_from_step(perc, cands, 100.0))
        nbytes = len(_json.dumps(rec["trace"], default=str))
        by_candidates.append({"n_candidates": c,
                              "us_per_decision_core": round(us_core, 2),
                              "us_per_decision_with_trace": round(us_traced, 2),
                              "trace_bytes": nbytes})
        print(f"  candidates={c}: core {us_core:.0f}us, +trace {us_traced:.0f}us, "
              f"{nbytes}B")

    base_cands = [{"action_id": f"r{k:04d}",
                   "score": float((k * 2654435761 % 1000) / 1000.0),
                   "source": "agent", "objective": "pedagogy"} for k in range(10)]
    by_routines = []
    for nr in [8, 16, 32, 64, 128]:
        path = make_padded_bundle_path(nr)
        core_p = DeployedARLPolicy(bundle_path=path, emit_traces=False)
        traced_p = DeployedARLPolicy(bundle_path=path, emit_traces=True)
        cs_p, perc_p = _steady_state(core_p)
        us_core = time_decide(core_p, cs_p, perc_p, base_cands)
        us_traced = time_decide(traced_p, cs_p, perc_p, base_cands)
        rec, _ = traced_p.decide(copy.deepcopy(cs_p),
                                 fv_from_step(perc_p, base_cands, 100.0))
        nbytes = len(_json.dumps(rec["trace"], default=str))
        by_routines.append({"n_routines": nr,
                            "us_per_decision_core": round(us_core, 2),
                            "us_per_decision_with_trace": round(us_traced, 2),
                            "trace_bytes": nbytes})
        print(f"  routines={nr}: core {us_core:.0f}us, +trace {us_traced:.0f}us, "
              f"{nbytes}B")
    return {"by_candidates": by_candidates, "by_routines": by_routines,
            "reps": REPS,
            "scope": "governance cycle in-process; service transport/persistence "
                     "overhead reported in the live deployment chapter"}


def fairness():
    rs = load_routine_set(ROUTINES)
    popA = make_population(seed=SEED + 1, n_learners=N_PER_GROUP, sigma=0.12, n_steps=80,
                           archetype_weights={"progressing": 0.7, "boundary_mastery": 0.3},
                           subgroup="A")
    popB = make_population(seed=SEED + 2, n_learners=N_PER_GROUP, sigma=0.12, n_steps=80,
                           archetype_weights={"boundary_mastery": 0.5, "boundary_affect": 0.5},
                           subgroup="B")

    def densities(make_pol):
        out = {}
        for label, pop in (("A", popA), ("B", popB)):
            dens, maxwin = [], []
            for stream in pop:
                res = make_pol().run(stream)
                dens.append(M.intervention_density_per_hour(res))
                maxwin.append(M.max_interventions_per_window(res, rs.budget_reset_minutes))
            m, ci = M.mean_ci(dens)
            out[label] = {"density_mean": round(m, 3), "density_ci": round(ci, 3),
                          "max_per_window": int(max(maxwin))}
        a, b = out["A"]["density_mean"], out["B"]["density_mean"]
        out["parity_ratio"] = round(min(a, b) / max(a, b), 4) if max(a, b) > 0 else 1.0
        out["density_gap"] = round(abs(a - b), 3)
        return out

    return {"ARL": densities(lambda: DeployedARLPolicy()),
            "B1": densities(lambda: B1DirectML(rs)),
            "budget_per_window": rs.budget_interventions}


def main():
    print("=== Study 5a: latency (deployed cycle) ===")
    lat = latency_table()
    print("=== Study 5b: fairness ===")
    fair = fairness()
    out = {"study": "study5_latency_fairness", "latency": lat, "fairness": fair}
    save_json("study5_latency_fairness.json", out)

    for pol in ("ARL", "B1"):
        f = fair[pol]
        print(f"  {pol}: A={f['A']['density_mean']:.2f} (max/win {f['A']['max_per_window']}), "
              f"B={f['B']['density_mean']:.2f} (max/win {f['B']['max_per_window']}), "
              f"parity={f['parity_ratio']:.2f}, gap={f['density_gap']:.2f}")
    return out


if __name__ == "__main__":
    main()
