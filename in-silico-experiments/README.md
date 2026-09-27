# X-ELRA simulation studies

This directory contains the simulation studies, property-based tests, and bounded model checker used in the computational evaluation of the thesis *Agentic Regulated Learning: A Governance Architecture for Process-Level Explainability in Adaptive Learning Systems* (Section 7.10 and Section 6.11.4).

This README covers running and reproducing only. The study design, measures, results, and their interpretation are reported in the thesis, which is the authoritative reference.

---

## What is tested

The studies exercise the governance modules of the enclosing repository (`../xelra/arl/` and `../xelra/olm/regulatory.py`), loaded unmodified at run time. The decision-cycle orchestration is replicated in `adapters/deployed_policy.py`, line-validated against `xelra/arl/engine.py::run_arl_cycle`, because the engine module itself requires the service database. The simulator, metrics, and comparator policies in `sim/` are measurement instruments only.

## Requirements

- Python 3.10 or later
- The packages in `requirements.txt`

```bash
pip install -r requirements.txt
```

## Run everything

```bash
python3 experiments/run_all.py
```

This runs the tests and model checker, then all six studies, then regenerates the sample decision records. Runs are seeded, so decision-level results are reproducible.

To regenerate the figures:

```bash
python3 experiments/make_figures.py
```

## Run one study

Each study can be run on its own, for example:

```bash
python3 experiments/study1_oscillation.py
```

| Script | Topic |
| --- | --- |
| `study1_oscillation.py` | Mode oscillation and predictability under perception noise |
| `study2_audit.py` | Audit sufficiency of decision records |
| `study3_sensitivity.py` | Sensitivity to governance parameters |
| `study4_robustness.py` | Asynchronous, missing, and multi-agent signals |
| `study5_latency_fairness.py` | Cost per decision and intervention exposure |
| `study6_fairness.py` | Intervention exposure across synthetic proficiency strata |

## Run the tests only

```bash
python3 tests/test_determinism.py
python3 tests/test_boundedness.py
python3 tests/verify_properties.py        # includes the bounded model check
python3 tests/test_adapter_regression.py
```

## Layout

```
adapters/        deployed_policy.py: runs the deployed governance modules
                 one decision cycle at a time
experiments/     the six studies, run_all.py, make_figures.py, gen_samples.py
sim/             simulator, metrics, and comparator policies (instruments only)
routines/        baseline configuration for the comparator policies
tests/           determinism, boundedness, property tests, model checker,
                 adapter regression
results/         JSON outputs of the canonical run
figures/         generated figures
sample_traces/   example decision records from the deployed modules
```

## Provenance

The module checksums, configuration identity, and seeds of the canonical run are recorded in the thesis (Appendix I). All inputs are synthetic; no learner data is included.

**Licence:** MIT (see `LICENSE`).
