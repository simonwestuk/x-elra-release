"""Study 3 -- Boundedness vs adaptivity: responsiveness, support, and stability.

Addresses the concern that deterministic boundedness may degrade responsiveness
or under-support learners in dynamic contexts, and the request for sensitivity
of results to the governance parameters (budgets, cooldowns, dwell time).

On streams with ground-truth genuine-need episodes we measure time-to-support
(delay from need onset to the first bounded intervention), the under-support
rate (fraction of episodes that received no support in-window), and stability
(mode oscillation rate and bounded-intervention density).

Part A compares the deployed controller against the baselines at default
configuration; Part B sweeps the deployed controller's governance parameters.
Each variant is a faithful parameterisation of the corresponding deployed
constant, applied without modifying the deployed sources: budget capacity is
applied wherever the deployed cycle installs fresh budgets, dwell parameterises
tau_dwell in the transition check (deployed constant 300 s), and cooldown
scaling rewrites a temporary copy of the deployed routine YAML.
"""

from __future__ import annotations

import numpy as np

from common import ROUTINES, SEED, save_json
from sim.dsl import load_routine_set
from sim.baselines import B1DirectML, B2RuleITS, B5SmoothedML
from sim.perception import make_multi_need_stream
from sim import metrics as M
from deployed_policy import DeployedARLPolicy, make_scaled_bundle_path

N_EP = 150
SIGMA = 0.12


def window_support_delay(steps, onset, end, grace=9.0):
    for s in steps:
        if s.t < onset:
            continue
        if s.t > end + grace:
            break
        if s.intervened:
            return s.t - onset
    return None


def eval_policy(policy, episodes):
    delays, n_windows, under, mors, dens = [], 0, 0, [], []
    for (stream, windows) in episodes:
        steps = policy.run(stream)
        for (onset, end) in windows:
            n_windows += 1
            d = window_support_delay(steps, onset, end)
            if d is None:
                under += 1
            else:
                delays.append(d)
        mors.append(M.mode_oscillation_rate(steps))
        dens.append(M.intervention_density_per_hour(steps))
    md, mci = M.mean_ci(delays) if delays else (float("nan"), 0.0)
    return {
        "mean_delay_min": round(md, 2), "delay_ci": round(mci, 2),
        "under_support_rate": round(under / max(n_windows, 1), 4),
        "mor": round(float(np.mean(mors)), 2),
        "density_per_h": round(float(np.mean(dens)), 2),
    }


def main():
    rs = load_routine_set(ROUTINES)
    episodes = [make_multi_need_stream(seed=SEED + i, sigma=SIGMA) for i in range(N_EP)]

    # --- Part A: policy comparison at default configuration ---
    polA = {
        "ARL": DeployedARLPolicy(),
        "B1": B1DirectML(rs),
        "B2": B2RuleITS(rs),
        "B5": B5SmoothedML(rs),
    }
    partA = {name: eval_policy(p, episodes) for name, p in polA.items()}

    # --- Part B: deployed-controller parameter sensitivity ---
    sweep = {"budget": [], "dwell": [], "cooldown_scale": []}
    for b in [1, 2, 3, 5, 8]:
        r = eval_policy(DeployedARLPolicy(budget_interventions=b), episodes)
        r["value"] = b
        sweep["budget"].append(r)
    for d in [0, 2, 5, 10, 15]:
        r = eval_policy(DeployedARLPolicy(dwell_seconds=d * 60), episodes)
        r["value"] = d
        sweep["dwell"].append(r)
    for c in [0.25, 0.5, 1.0, 2.0, 4.0]:
        r = eval_policy(DeployedARLPolicy(bundle_path=make_scaled_bundle_path(c)), episodes)
        r["value"] = c
        sweep["cooldown_scale"].append(r)

    out = {
        "study": "study3_sensitivity",
        "design": {"n_episodes": N_EP, "sigma": SIGMA,
                   "defaults": {"budget": 5, "dwell_minutes": 5,
                                "cooldown_scale": 1.0},
                   "variant_mechanism": "budget/dwell parameterise the deployed "
                                        "constant in the adapter (defaults use the "
                                        "deployed code path); cooldown scaling uses "
                                        "a temporary YAML copy"},
        "policy_comparison": partA,
        "sweep": sweep,
    }
    save_json("study3_sensitivity.json", out)

    print("=== Study 3a: responsiveness vs stability (default config) ===")
    print(f"{'policy':>9} | {'delay(min)':>10} {'under-supp':>10} {'MOR/h':>7} {'dens/h':>7}")
    for name, r in partA.items():
        print(f"{name:>9} | {r['mean_delay_min']:>10.2f} {r['under_support_rate']:>10.2f} "
              f"{r['mor']:>7.2f} {r['density_per_h']:>7.2f}")
    print()
    print("=== Study 3b: deployed parameter sweeps ===")
    for r in sweep["budget"]:
        print(f"  budget={r['value']}: delay {r['mean_delay_min']:.2f} min, "
              f"under-support {r['under_support_rate']:.2f}, dens {r['density_per_h']:.2f}")
    print("--- dwell sweep ---")
    for r in sweep["dwell"]:
        print(f"  dwell={r['value']}min: delay {r['mean_delay_min']:.2f}, "
              f"under-support {r['under_support_rate']:.2f}, MOR {r['mor']:.2f}")
    print("--- cooldown-scale sweep ---")
    for r in sweep["cooldown_scale"]:
        print(f"  cooldown x{r['value']}: delay {r['mean_delay_min']:.2f}, "
              f"under-support {r['under_support_rate']:.2f}, dens {r['density_per_h']:.2f}")
    return out


if __name__ == "__main__":
    main()
