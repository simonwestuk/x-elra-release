# X-ELRA controller: simulation studies

This directory tests the X-ELRA controller on simulated learners. X-ELRA is
the deployed implementation of Agentic Regulated Learning (ARL), and the
governance modules tested here are the enclosing repository's own code, the
exact modules that governed the live deployment reported in the thesis. A
live course cannot stress-test a controller, so these studies do it in
simulation: the controller's governance modules are loaded verbatim at run
time (no copies, no modification), a seeded simulator generates learners
whose measurements are deliberately noisy, and the controller is compared
against three simpler policies on identical input.

The suite is one adapter file (`adapters/deployed_policy.py`) that drives
the deployed controller through its production decision cycle, six studies
that evaluate it against simple comparator policies, and a verification
layer (property tests and a bounded model checker) that runs on the same
deployed code. The simulator, metrics, and comparators are instruments; no
second ARL controller exists anywhere in this suite.

## Layout

```
adapters/   deployed_policy.py -- runs one production decision cycle per
            simulated step (persistent controller state across steps) and
            emits the controller's full decision record
experiments/  the six studies, run_all, figure generation
sim/        the simulator, metrics, and comparator baseline policies
            (instruments only; the ARL controller under test is the
            deployed engine in ../xelra/, loaded by the adapter)
routines/   baseline configuration (x_elra.yaml); shared values identical
            to the production configuration
tests/      determinism + boundedness property tests and the bounded model
            checker, all exercising the deployed controller; adapter
            regression
results/    JSON results, one file per study
figures/    fig6-fig10 (fig6 study 1, fig7 study 2, fig10 study 3,
            fig8/fig9 study 5)
```

The governance modules under test are `../xelra/arl/` and
`../xelra/olm/regulatory.py`, together with `../config/arl_routines.yaml`,
loaded by the adapter exactly as they stand in this repository.
`routines/x_elra.yaml` does not configure the controller under test; it
configures the baseline policies and the analysis windows, and its shared
values (budgets, per-routine costs, and cooldowns) are identical to the
production configuration.

## Reproduce

```bash
pip install numpy pyyaml matplotlib
python3 experiments/run_all.py       # tests + all six studies, seed 20260601
python3 experiments/make_figures.py  # figures -> ./figures
```

Every study is seeded, and all decision-level results are bit-reproducible
across runs and machines; the only exception is the wall-clock latency
timings of study 5, which vary with the host machine.

## What each study shows

The runner order in [experiments/run_all.py](experiments/run_all.py) is:
1. `study1_oscillation`
2. `study2_audit`
3. `study3_sensitivity`
4. `study4_robustness`
5. `study5_latency_fairness`
6. `study6_fairness`

| Study | Question | Headline result |
|------|----------|-----------------|
| 1 (`study1_oscillation`) | Does deterministic regulation reduce intervention oscillation and improve predictability under perception noise? (H2) | At sigma=0.15, mode-oscillation rate 2.6/h vs 18.6/h for a direct-ML policy (7.1x lower), rising only from 0.8 to 2.8/h across the noise grid, with zero immediate stance reversals anywhere; next-stance predictability 0.62 vs 0.01; intervention density 0.27/h, max 1 per budget window (the smoothed policy reaches 2.3/h but at up to 4 per window and with no decision trace). |
| 2 (`study2_audit`) | Are decision traces sufficient to reconstruct a decision, vs standard logs? (H4) | Per-property (DEMM-style) reconstructability 1.00 on all five properties, **measured per record** from 16,000 emitted decision records rather than granted by construction; 99% of decisions are deliberate non-interventions invisible to action-only logs; an intervention localises from a single record vs scanning ~32 (and failing) for a model log. |
| 3 (`study3_sensitivity`) | How do responsiveness, support, and boundedness trade off as the governance parameters vary? | Cooldowns are the operative dial and have an interior optimum: half-scale cooldowns cut the under-support rate to 0.22 at 1.24 interventions/h, double-scale raises it to 0.75, and quarter-scale worsens it again (0.45) because early interventions exhaust budgets and trip the overload stance. Budget capacity is non-binding above one, because the deployed engine refills budgets on stance changes and session boundaries. |
| 4 (`study4_robustness`) | Does determinism survive asynchronous/missing/multi-agent signals? | Replay from persisted pre-decision state reproduces all 12,000 decisions (trace hash, item hash, executed routine); candidate arrival order never changes a decision or its canonical hash (4,800/4,800); the missing-modality guard routes 100% of 1,920 outage decisions to DIAGNOSTIC with zero pedagogical actions on incomplete data in 120/120 episodes (the bounded integrity probe fires on 6%, the guard acting) while the ungoverned direct policy acts in 120/120 episodes; a late signal changes nothing retroactively and both runs replay exactly. |
| 5 (`study5_latency_fairness`) | What does it cost, and is exposure bounded across subgroups? | ~31 microseconds per governance decision, flat to 500 candidates and 72 us at 128 routines; emitting the full audit record adds 0.1 to 1.6 ms as the payload grows to 46 KB, so a complete governed decision stays under 2 ms. Per-subgroup intervention density at parity 0.99 with an equal ceiling of 2 per window, vs an unbounded 15-16 per window for the direct-ML policy. |
| 6 (`study6_fairness`) | Are interventions distributed fairly across proficiency strata? | Worst-case exposure is capped at 2 per window for every stratum, with densities 0.53-0.80/h (parity 0.66) against 15.9-35.4/h (parity 0.45) for direct-ML. Supporting-stance occupancy runs 0.14/0.31/0.66 across low/medium/high proficiency, a profile that differs from the paper's standalone implementation; the mechanism (the deployed dwell anchoring) and its scoping are analysed in the thesis. |
| `tests/` | Safety, liveness, and adapter fidelity, on the deployed controller | Determinism, serialised replay, and candidate-order invariance hold over 3,000 randomised cases; over 960 random streams, budgets stay in range everywhere, no routine fires within its cooldown, interventions peak at 3 per 30-minute window (capacity 5), and stance changes are never closer than the 300 s dwell; bounded model checking explores 25,886 reachable states exhaustively within bound (horizon 16 steps, 7-input adversarial alphabet, clock pinned to decision time) with 0 safety violations, and every reachable COOLDOWN state exits within 3 steps at the deployment's request-driven cadence and within 7 under sub-dwell recovery (bound 20); the adapter regression pins the deployed cycle to validated reference values. |

## Provenance, licence, data

The controller under test is this repository's own governance code, loaded
verbatim at run time; the simulator, metrics, and baseline policies in
`sim/` are instruments only, with no controller implementation of
their own. All
inputs are synthetic; no learner data is included. The module checksums,
configuration identity, and seeds of the canonical run are recorded in
the thesis. MIT Licence (see `LICENSE`).
