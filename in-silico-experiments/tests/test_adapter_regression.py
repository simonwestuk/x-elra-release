"""Adapter regression: the deployed-cycle adapter must reproduce validated
reference values on a fixed protocol (10 learners x 80 steps, seeds 20260601+).
Guards against any edit that changes the adapter's behaviour."""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "adapters"))
ROUTINES = os.path.join(ROOT, "routines", "x_elra.yaml")
import numpy as np
from sim.dsl import load_routine_set
from sim.perception import make_stream
from sim import metrics as M
from deployed_policy import DeployedARLPolicy

EXPECT = {  # from the engine-faithful spike re-run (10 x 80, seeds 20260601+)
    0.05: dict(mor=0.759, rev=0.000, ipi=0.778, dens=0.405, maxwin=0.800),
    0.15: dict(mor=2.380, rev=0.000, ipi=0.635, dens=0.203, maxwin=0.400),
}

rs = load_routine_set(ROUTINES)
window = rs.budget_reset_minutes
ok = True
for sigma, exp in EXPECT.items():
    pol = DeployedARLPolicy()
    agg = {k: [] for k in exp}
    for i in range(10):
        stream = make_stream(seed=20260601 + i, archetype="boundary_mastery",
                             sigma=sigma, n_steps=80)
        res = pol.run(stream)
        agg["mor"].append(M.mode_oscillation_rate(res))
        agg["rev"].append(M.immediate_reversals(res))
        agg["ipi"].append(M.ipi_stance(res))
        agg["dens"].append(M.intervention_density_per_hour(res))
        agg["maxwin"].append(M.max_interventions_per_window(res, window))
    got = {k: float(np.mean(v)) for k, v in agg.items()}
    for k, v in exp.items():
        match = abs(got[k] - v) < 5e-3
        ok = ok and match
        print(f"sigma={sigma} {k:7}: got {got[k]:.3f} expect {v:.3f} {'OK' if match else 'MISMATCH'}")
print("REGRESSION", "PASS" if ok else "FAIL")

# trace emission sanity
pol = DeployedARLPolicy(emit_traces=True)
res = pol.run(make_stream(seed=20260601, archetype="boundary_affect", sigma=0.12, n_steps=20))
tr = next(s.trace for s in res if s.intervened)
print("trace keys:", sorted(tr.keys()))
print("olm mode_label:", tr["olm_projection"].get("mode_label"))
print("exit conds:", tr["next_transition_conditions"][:2])
print("path:", [(p["routine_name"], p["outcome"]) for p in tr["routine_path"]])
