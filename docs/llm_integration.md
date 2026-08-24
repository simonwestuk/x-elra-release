# LLM Feedback Generator — Integration Architecture

## Architectural Rationale

This integration validates the ARL controller's **separation contract**: the
claim that upstream ML components can be added, removed, or swapped without
modifying the deterministic governance controller.  The LLM feedback generator
is a new upstream candidate producer that sits alongside the existing hybrid
recommender.  The controller evaluates LLM-generated candidates using the same
routines, mode gating, cooldowns, and budgets that govern recommender
candidates — with zero changes to `xelra/arl/`.

## Pipeline Position

```
BEFORE (main branch):
  Hybrid Recommender → candidate actions ──────────────────→ C_t
  Knowledge Tracing → mastery estimates ───────────────────→ O_t  → I_t → Controller → A_t + T_t
  DistilBERT → affect flags ───────────────────────────────→ O_t

AFTER (this branch):
  Hybrid Recommender → candidate actions ──────┐
                                               ├─ merged → C_t
  LLM Feedback Generator → feedback candidate ─┘
  Knowledge Tracing → mastery estimates ───────────────────→ O_t  → I_t → Controller → A_t + T_t
  DistilBERT → affect flags ───────────────────────────────→ O_t
```

## What Was Modified

| File | Change |
|------|--------|
| `xelra/models/llm/__init__.py` | New package |
| `xelra/models/llm/config.py` | LLM configuration + feature flag |
| `xelra/models/llm/prompts.py` | Prompt templates (governance-free) |
| `xelra/models/llm/feedback_generator.py` | Main generator class |
| `xelra/arl/state.py` | Candidate merge step in `build_feature_vector()` |
| `tests/test_llm_feedback.py` | Unit + integration tests |

## What Was NOT Modified

All files in `xelra/arl/` remain identical to main:

- `xelra/arl/engine.py` — ARL cycle orchestration
- `xelra/arl/controller_state.py` — Controller state S_t
- `xelra/arl/schemas.py` — Trace and routine schemas
- `xelra/arl/boundedness.py` — Budget/cooldown/oscillation enforcement
- `xelra/arl/mode_inference.py` — Mode transition function
- `config/arl_routines.yaml` — Routine definitions

## Candidate Merge Logic

After the hybrid recommender produces its candidate list, the LLM feedback
generator (when enabled) produces one additional candidate.  The two lists are
merged with:

1. **Score-descending sort** — higher-scored candidates appear first
2. **Deterministic tie-breaking** — equal scores are broken lexicographically
   by `item_id`, ensuring replay consistency

The merged list is stored in `FeatureVector.recommendations`.  The controller
consumes this field identically to before — it does not know or care which
upstream component produced a given candidate.

## Provenance Tracking via `source` Field

Each candidate in the merged list carries a `source` field:

- `"hybrid_recommender"` — existing recommender candidates (added as a
  backward-compatible default)
- `"llm_feedback_generator"` — LLM-generated feedback candidates

The `source` field survives into the decision trace because the full
`FeatureVector` (including `recommendations`) is stored in:

1. `ARLCycleResult.feature_vector`
2. The persisted `request_payload` in the `ARLDecision` table
3. The compact `decision_trace` under `inputs_summary`

### Separation-Contract Gap: Trace Decision Object

The compact decision trace's `decision` object records:

```json
{"action": "fetch_recommendations", "source_routine": "P7_default_hybrid"}
```

This captures *which routine* selected the action, but not *which individual
candidate* from the recommendations list was ultimately surfaced.  The `source`
field on individual candidates does not propagate into the `decision` object.

**Finding:** The current trace schema does not record per-candidate provenance
in the compact decision output.  Adding source tracking to the `decision`
object (e.g., `"candidate_source": "llm_feedback_generator"`) would require
extending the trace construction in `engine.py`, which constitutes a controller
modification.  This identifies a gap in the separation contract: while the
controller evaluates candidates agnostically, the trace does not record which
upstream component proposed the candidate that was ultimately surfaced to the
learner.

To fully resolve this, a future change to `engine.py` would need to thread the
selected item's `source` field into the `decision` dict.  This is a minor,
additive change but was deliberately not made in this integration to honour the
constraint.

## Enabling the Feature

Set the environment variable before starting the server:

```bash
export XELRA_LLM_FEEDBACK=true
```

When `XELRA_LLM_FEEDBACK` is unset or `"false"`, the pipeline behaves
identically to main — no LLM calls, no extra candidates, no merge step.

### Ollama Setup

1. Install Ollama: https://ollama.ai
2. Pull a model: `ollama pull llama3`
3. Ollama runs on `http://localhost:11434` by default

Optional environment variables for LLM configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `XELRA_LLM_MODEL` | `llama3` | Ollama model name |
| `XELRA_LLM_BASE_URL` | `http://localhost:11434` | Ollama API endpoint |
| `XELRA_LLM_TEMPERATURE` | `0.7` | Generation temperature |
| `XELRA_LLM_MAX_TOKENS` | `200` | Max tokens per generation |
| `XELRA_LLM_TIMEOUT` | `10` | Request timeout in seconds |

## Graceful Degradation

If the LLM is unavailable, slow, or returns empty/invalid output, the
generator returns an empty candidate list.  The merge step simply produces the
recommender-only list.  The pipeline continues without interruption.  This is
logged at WARNING level for monitoring.
