# X-ELRA: Explainable E-Learning Recommendation Architecture

X-ELRA is the reference implementation of Agentic Regulated Learning (ARL): machine learning components produce perceptions and candidate actions, and a deterministic, bounded controller decides whether, when, and how to intervene, recording every decision (including deliberate non-intervention) as a replayable trace projected to the learner through an Open Learner Model. This repository is the system deployed in the thesis's live feasibility study, and its governance modules are exercised verbatim by the simulation studies in [`in-silico-experiments/`](in-silico-experiments/README.md).

This README is operational only: how to install, run, inspect, and reproduce. The architecture, formal specification, algorithms, terminology, and evaluation are documented in the thesis, which is the single source of truth for everything conceptual.

**Thesis**: <THESIS_CITATION>
**ARL specification and standalone evaluation suite**: <PAPER_REPO_URL>
**Archive**: <ZENODO_DOI>
**Licence**: MIT (see `LICENSE`)

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [In-Silico Experiments](#in-silico-experiments)
3. [Repository Map](#repository-map)
4. [API Reference](#api-reference)
5. [Control Routine Overview](#control-routine-overview)
6. [Module Map](#module-map)
7. [Recommendation Configuration](#recommendation-configuration)
8. [Demo Learners & Control Routines](#demo-learners--control-routines)
9. [Standalone Experience](#standalone-experience)
10. [Lesson Content](#lesson-content)
11. [Accessibility](#accessibility)
12. [Certificate of Participation](#certificate-of-participation)
13. [Engagement Monitoring](#engagement-monitoring)
14. [Post-Study Feature Unlock](#post-study-feature-unlock)
15. [Configuration Reference](#configuration-reference)
16. [Privacy & Compliance](#privacy--compliance)
17. [Testing](#testing)

---

## Quick Start

### Requirements

- Python **3.10+**
- SQLite (bundled)
- Optional: SMTP account for magic-code login

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create `.env` manually (no `.env` template is distributed in this public-release archive) or export variables in your shell:

```bash
export DATABASE_URI="sqlite:///./data/xelra_app.db"
export FEATURE_STORE_URI="sqlite:///./data/xelra_fs.db"
export SMTP_HOST="smtp.example.com"
export SMTP_USER="username"
export SMTP_PASS="password"
export SMTP_FROM="noreply@example.com"
export LOGIN_JWT_SECRET="change-me-login"
```

Optional (enable online sentiment):

```bash
export HUGGING_FACE_HUB_TOKEN="hf_token"
export SENTIMENT_MODEL_NAME="distilbert-base-uncased-finetuned-sst-2-english"
```

### Seed Demo Data

Populate skills, items, learners, and control routine scenarios:

```bash
python scripts/seed_demo_data.py
```

By default this **drops and recreates all tables**. To seed without wiping existing data:

```bash
python scripts/seed_demo_data.py --no-reset
# or via environment variable:
export SEED_NO_RESET=1
python scripts/seed_demo_data.py
```

This seeds:
- **PY101**: Python Fundamentals course (7 skills, 192 items, 8 learners) using Skulpt engine
- All 8 control routines (P1-P8) demonstrated by specific learners
- All 9 controller modes (COLD_START through COOLDOWN) represented

### Start the Server

```bash
uvicorn xelra.server.app:app --host 0.0.0.0 --port 8000 --reload
```

Useful URLs:

- Standalone app: `http://localhost:8000/app/web/standalone.html`
- API docs: `http://localhost:8000/docs`

---


## In-Silico Experiments

[`in-silico-experiments/`](in-silico-experiments/README.md) contains the six controlled simulation studies reported in the thesis (stability and predictability, audit sufficiency, sensitivity, robustness, cost and subgroup exposure, and fairness across proficiency strata). They load this repository's governance modules verbatim at run time and drive them through the production decision cycle against seeded synthetic learners; nothing in `xelra/` is modified. Every decision-level result is seeded and bit-reproducible:

```bash
cd in-silico-experiments
pip install numpy pyyaml matplotlib
python3 experiments/run_all.py       # tests + all six studies
python3 experiments/make_figures.py  # figures
```

See that directory's README for the study-by-study questions and results, and the thesis for the configuration provenance (module checksums, seeds) and analysis.

---


## Repository Map

```
xelra/                  application package: FastAPI server, ARL controller
                        (xelra/arl/), OLM projection (xelra/olm/),
                        recommenders and sentiment (xelra/models/), telemetry
config/                 production routine bundle (arl_routines.yaml) and
                        experiment arm configuration (arms.yaml)
content/                PY101 course source (Markdown)
static/                 frontend (standalone app, assets); lesson HTML is
                        generated locally by scripts/build_content.py
scripts/                seeding (seed_demo_data.py), content build
                        (build_content.py), server launcher (run_server.sh)
docs/                   service API contract; optional LLM extension notes
in-silico-experiments/  the thesis's six simulation studies (own README)
data/                   created at runtime by the server (databases);
                        not distributed
```

---


## API Reference

### Agentic Regulated Learning (ARL)

`POST /v1/arl` runs one governed decision cycle for a learner and returns the full decision record; the controller's behaviour, state, and trace fields are specified in the thesis.

#### API Usage

Learner endpoints require the bearer token from `/v1/standalone/verify_code` (or one minted via `xelra.utils.auth.issue_login_token`).

```bash
# Run a deterministic cycle
curl -X POST /v1/arl \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"learner_id": "<uuid>", "refresh_features": true}'

# Emit an event-driven cycle
curl -X POST /v1/arl/event \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"learner_id":"<uuid>", "event_type":"completion"}'
```

Optional flags: `override_arm`, `verify_assignment`.

**Response includes controller state:**

```json
{
  "learner_id": "...",
  "decision_id": "...",
  "deterministic_hash": "sha256:...",
  "routine_version": "3.0.0",
  "seed": 12345,
  "controller_state_before": {
    "mode": "struggling",
    "budgets": {"interventions_remaining": 4, "suggestions_remaining": 7},
    "timers": {"last_intervention": "2026-01-06T12:00:00Z"},
    "recent_outcomes": {"decision_history": ["P7", "P3"]}
  },
  "controller_state_after": {
    "mode": "nominal",
    "budgets": {"interventions_remaining": 3, "suggestions_remaining": 4},
    "timers": {"last_intervention": "2026-01-06T14:30:00Z"},
    "recent_outcomes": {"decision_history": ["P7", "P3", "P3"]}
  },
  "routine_results": [...],
  "explanations": [...]
}
```

#### Enabling Formal ARL

Set the feature flag in your environment:

```bash
export ENABLE_FORMAL_ARL=1
```

When enabled, the ARL engine:
- Loads/persists controller state from the `controller_states` table
- Enforces mode-based routine gating
- Applies cooldown periods between routine executions
- Tracks resource budgets (interventions, suggestions)
- Detects and prevents oscillation patterns
- Ensures minimum mode stability (5 minutes between transitions)

#### Controller Modes

The controller operates in one of nine modes, each permitting specific control routines:

| Mode | OLM Label | Description | Permitted Routines | Entry Conditions |
| --- | --- | --- | --- | --- |
| **COLD_START** | Discovering | New learner, no telemetry | P1 (Orientation) | Empty mastery + 0 impressions in 30 days |
| **ORIENTATION** | Exploring | Initial onboarding | P1 (Orientation), P7 (Default) | Empty mastery + 1-9 impressions (early engagement) |
| **NOMINAL** | Progressing | Steady-state learning | P7 (Default) | Normal engagement, balanced mastery |
| **STRUGGLING** | Supporting | Requires intervention | P3 (Uplift), P8 (Affective Overload) | Lowest mastery < 0.4 + no clicks in 14 days, **or** confusion/frustration detected (affect flags) |
| **LAPSED** | Reconnecting | Re-engagement needed | P4 (Re-engagement) | >15 days since last engagement, active goals |
| **ACCELERATING** | Advancing | High momentum | P5 (Accelerator) | Active goals, progress rate ≥ 0.05/day |
| **CONSOLIDATING** | Reinforcing | Mastery reinforcement | P6 (Consolidation) | Highest mastery ≥ 0.85, recent completions |
| **DIAGNOSTIC** | Assessing | Data integrity check | P2 (Diagnostics), P7 (Default) | Feature gap > 2 (multiple missing learner data sources) |
| **COOLDOWN** | Resting | Over-intervention protection | P7 (Default) | Oscillation detected (>3 mode transitions in 30 min) or budget exhaustion (≤1 intervention + ≥3 transitions) |

Mode transitions are deterministic and based on learner perceptions (feature vector metadata).

#### Resource Budgets

Per-session budgets prevent over-intervention:

| Resource | Default Limit | Reset Condition | Enforced By |
| --- | --- | --- | --- |
| **interventions** | 5 / session | 4 hours since last intervention | P1, P2, P3, P4, P8 |
| **suggestions** | 10 / week | Weekly (Monday UTC 00:00) | P3, P5, P6, P8 |

Control routines consuming exhausted budgets are automatically blocked.

#### Routine Cooldowns

Minimum time between control routine executions:

| Routine | Cooldown | Rationale |
| --- | --- | --- |
| **P1** (Orientation) | 24 hours | Daily orientation updates |
| **P2** (Diagnostics) | 1 hour | Frequent integrity checks allowed |
| **P3** (Uplift) | 4 hours | Intervention spacing |
| **P4** (Re-engagement) | 7 days | Weekly re-engagement maximum |
| **P5** (Accelerator) | 1 hour | Frequent momentum updates |
| **P6** (Consolidation) | 2 hours | Practice drill spacing |
| **P7** (Default) | None | Always available fallback (permitted in NOMINAL, COOLDOWN, ORIENTATION, DIAGNOSTIC) |
| **P8** (Affective Overload) | 2 hours | Affect intervention spacing |

### Recommendation Endpoints

- `POST /v1/recommend/recommendations/by_group`: supply `{"learner_id": "...", "group": "treatment"}` to map to a strategy/explain combo.
- `POST /v1/recommend/recommendations`: legacy entry point when you want to set `strategy` and `explain` explicitly.
- `POST /v1/recommend/next_up`: sequence-only next item.

Helper:

```python
from xelra.experiment.groups import ExperimentGroup

req = ExperimentGroup.treatment.to_request("learner-id", top_k=5)
```

---


## Control Routine Overview

| ID | Title | Priority | Permitted Modes | Cooldown | Resource Costs | Trigger Summary | Primary Actions |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **P1** | Orientation Safety Net | 120 | COLD_START, ORIENTATION | 24h | interventions: 1 | Empty mastery (mode gating restricts to learners with 0-9 impressions) | Fetch orientation playlist (sequence) |
| **P2** | Data Integrity Checks | 110 | DIAGNOSTIC | 1h | interventions: 1 | Feature gap > 2 (missing learner data sources) | Fetch diagnostics bundle |
| **P8** | Affective Overload Intervention | 95 | STRUGGLING | 2h | interventions: 1, suggestions: 1 | `frustration_flag == true` or `confusion_flag == true` (affect flags from live code errors + sentiment) | Wellbeing break + fundamentals reset |
| **P3** | Struggling Learner Uplift | 90 | STRUGGLING | 4h | interventions: 1, suggestions: 3 | `mastery \| lowest < 0.4`, no clicks in 14 days, and impressions in 30 days > 5 | Fundamentals refresh set |
| **P4** | Lapsed Learner Re-engagement | 80 | LAPSED | 7d | interventions: 1 | `metadata.days_since_last_engagement > 15` and active goals | Hybrid re-engagement playlist |
| **P5** | Goal Attainment Accelerator | 70 | ACCELERATING | 1h | suggestions: 2 | Active goals with `progress_rate ≥ 0.05` | Goal-focused acceleration set |
| **P6** | Mastery Consolidation | 60 | CONSOLIDATING | 2h | suggestions: 2 | `mastery \| highest ≥ 0.85` and completions in last 7 days | Consolidation / drill playlist |
| **P7** | Default Hybrid Pathway | 10 | NOMINAL, COOLDOWN, ORIENTATION, DIAGNOSTIC | None | None | Universal fallback ensuring participants always receive recommendations | Balanced hybrid recommendations |

Control routines are defined in `config/arl_routines.yaml` (schema 3.0) and evaluated by `xelra.arl.engine.run_arl_cycle`. When `ENABLE_FORMAL_ARL=1`, the engine enforces mode-based gating, cooldowns, and resource budgets before routine execution.

---


## Module Map

Where each part of the governed decision cycle lives:

| Component | Location |
| --- | --- |
| ARL decision cycle (`run_arl_cycle`) | `xelra/arl/engine.py` |
| Controller state (mode, budgets, timers, history) | `xelra/arl/controller_state.py` |
| Mode inference and state transition | `xelra/arl/mode_inference.py` |
| Boundedness (budgets, cooldowns, oscillation, dwell) | `xelra/arl/boundedness.py` |
| Perception assembly (`FeatureVector`) | `xelra/arl/state.py`, `xelra/arl/schemas.py` |
| Routine set, DSL, and loading | `config/arl_routines.yaml`, `xelra/arl/dsl.py`, `xelra/arl/routines.py` |
| Condition evaluation | `xelra/arl/conditions.py` |
| Routine actions | `xelra/arl/actions.py` |
| Decision trace schema (`ARLCycleResult`) | `xelra/arl/schemas.py` |
| Learner-facing OLM projection | `xelra/olm/regulatory.py` |
| Post-decision evaluation | `xelra/arl/evaluation.py`, `xelra/arl/evaluation_worker.py` |
| Hybrid recommender | `xelra/models/recommender/hybrid_simple.py` |
| Sequence fallback recommender | `xelra/models/recommender/sequence.py` |
| Optional LLM feedback generator | `xelra/models/llm/` (see `docs/llm_integration.md`) |

Reading decision records: each routine in the evaluation path carries one of four outcomes. SKIPPED (ineligible: unmet triggers or mode mismatch), BLOCKED (eligible but prevented by a budget, cooldown, or stability constraint, with the reason recorded), EXECUTED_ACTION, or EXECUTED_NO_ACTION (deliberate non-intervention). A decision that does nothing still emits a full record.

---


## Recommendation Configuration

All three experiment groups run the same sentiment-aware hybrid recommender with identical weights; only the explanation and governance layers differ, so observed differences are attributable to explanation type rather than recommendation quality.

| Group | Strategy | Sentiment Model | Sentiment Display | Regulatory Mode | XAI | Description |
| --- | --- | --- | --- | --- | --- | --- |
| **T: Treatment (ARL)** | Hybrid | Enabled (20%) | Process-level panel | Yes | SHAP | Process-level regulatory explanations (mode/why/next/exit) with sentiment panel and SHAP attribution. |
| **A: Control A (B1)** | Hybrid | Enabled (20%) | Post-hoc in SHAP | No | SHAP | Traditional post-hoc SHAP feature attribution (including S weight). No regulatory mode or sentiment panel. |
| **B: Control B (B3)** | Hybrid | Enabled (20%) | Hidden | No | None | OLM-only transparency: learner state display. Same recommender underneath but never surfaced. |

| Group | w_content | w_cf | w_popularity | w_sentiment |
| --- | --- | --- | --- | --- |
| T: Treatment (ARL) | 0.45 | 0.25 | 0.10 | 0.20 |
| A: Control A (B1) | 0.45 | 0.25 | 0.10 | 0.20 |
| B: Control B (B3) | 0.45 | 0.25 | 0.10 | 0.20 |

The final score is a transparent weighted sum of four normalised signals (content similarity, item-item collaborative filtering, popularity, sentiment alignment) computed in `xelra/models/recommender/hybrid_simple.py`, with deterministic lexicographic tie-breaking; equal-scored cold-start candidates fall back to curriculum order, and `xelra/models/recommender/sequence.py` provides the non-personalised fallback. Weights live in `config/arms.yaml`. The method itself is documented in the thesis.

---


## Demo Learners & Control Routines

After seeding, use the OTP printed in the server log to sign in as any demo learner.

### PY101 Learners by Controller Mode

Each demo learner is configured to demonstrate a specific controller mode and control routine:

| Email | Control Routine | Mode | Group | Entry Conditions |
| --- | --- | --- | --- | --- |
| `frank@example.com` | P1: Orientation Safety Net | COLD_START | T (Treatment) | Empty mastery + 0 impressions |
| `olivia@example.com` | P1: Orientation (early) | ORIENTATION | T (Treatment) | Empty mastery + 3 impressions → continued onboarding |
| `alice@example.com` | P2: Data Integrity | DIAGNOSTIC | A (Control A) | Feature gap > 2 (missing completions, no goals) |
| `bob@example.com` | P3: Struggling Uplift | STRUGGLING | A (Control A) | Lowest mastery < 0.4, no clicks in 14 days |
| `carol@example.com` | P4: Lapsed Re-engagement | LAPSED | B (Control B) | >15 days since last engagement, active goal set |
| `dave@example.com` | P5: Goal Accelerator | ACCELERATING | T (Treatment) | Active goals, progress rate ≥ 0.05/day (3 recent completions) |
| `eve@example.com` | P6: Mastery Consolidation | CONSOLIDATING | B (Control B) | Highest mastery ≥ 0.85, recent completions |
| `notag@example.com` | P7: Default Hybrid | NOMINAL | A (Control A) | Balanced mastery, normal engagement (steady-state fallback) |


Each learner has reflections, goal events, sentiment data, and historical ARL decisions so the Explain panel and Open Learner Model (OLM) show realistic context.

---


## Standalone Experience

The frontend lives under `static/` and uses the following flow:

1. **Login:** `/v1/standalone/request_code` issues a one-time code; `/v1/standalone/verify_code` returns a JWT (`sub`, `arm_key`, `aud=xelra-login`).
2. **Consent:** the UI polls `/v1/telemetry/consent/{learner_id}` and blocks interactions until the learner agrees. Revoking consent purges recent sentiment traces. The consent iframe automatically appends `?group=<arm_key>` (e.g. `?group=T`) so the external JISC form can identify the participant's experimental group.
3. **Surveys:** periodic survey iframes also append `?group=<arm_key>` to their URLs. Survey schedule and URL are configured via environment variables (`SURVEY_URL`, `SURVEY_WEEKS`, `SURVEY_ENABLED`); see [Configuration Reference](#configuration-reference).
4. **Cycle refreshes:** the app automatically posts to `/v1/arl` on login, goal changes, completions, and key feedback events so control routines remain up-to-date.
5. **Explain panel:** combines recommendation metadata, SHAP insights, and control routine rationale (captured from the latest ARL cycle).
6. **Interactive Python:** Lessons include live code blocks powered by configurable engines:
   - **Pyodide**: Full scientific Python with numpy/pandas/matplotlib (~13MB). Configured via `<meta name="xelra-md-live" data-engine="pyodide">`.
   - **Skulpt** (PY101): Lightweight browser Python for beginners (~500KB). Core Python only, no external libraries. Configured via `<meta name="xelra-md-live" data-engine="skulpt">`.

Sign out clears _all_ local storage (`token`, `learner_id`, cached control routines) to avoid stale state.

---


## Lesson Content

The platform ships one course: PY101 (Python Fundamentals), 7 modules, 48 topics, 192 resources (4 per topic: lesson, practice, challenge, reference), running on the Skulpt in-browser Python engine. Markdown source lives in `content/PY101/`; the built lesson HTML is not distributed, so generate it once before serving lessons:

```bash
python scripts/build_content.py
```

---


## Accessibility

The standalone frontend includes an accessibility toolbar (`static/js/ui/a11y-toolbar.js`) that provides:

- **Font scaling**: four steps (100%, 115%, 130%, 150%) persisted in `localStorage`
- **Text-to-speech**: reads the main content area aloud via the Web Speech API; toggle start/stop

The toolbar appears as a floating icon in the bottom-left corner. Preferences survive page reloads.

---


## Certificate of Participation

Learners who complete all items in a course (or all items globally) can view and print a participation certificate.

**Frontend:** `/static/web/certificate.html`, which auto-checks eligibility and issues the certificate. Printable via browser print dialog.

**API endpoints:**

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/v1/certificate/check` | Check eligibility (without issuing) |
| `POST` | `/v1/certificate/issue` | Issue certificate if all items completed |
| `GET` | `/v1/certificate/{learner_id}` | Retrieve existing certificate |

Request body for `check` and `issue`:

```json
{"learner_id": "...", "course_id": "PY101", "holder_name": "Jane Doe"}
```

The optional `holder_name` field sets the display name on the certificate. When a learner is eligible, the certificate page prompts them to enter their name before issuing. Omit `course_id` to check global completion across all courses. Certificates are stored in the `certificates` table with a unique constraint on `(learner_id, course_id)`.

---


## Engagement Monitoring

A background task runs daily to identify inactive learners and send engagement reminder emails. The system classifies each learner into risk tiers based on days since their last activity (completion or click).

| Risk Level | Days Inactive | Action |
| --- | --- | --- |
| **active** | 0-3 | None |
| **warning** | 4-7 | Email reminder (7-day cooldown) |
| **critical** | 8-14 | Email reminder (7-day cooldown) |
| **lost** | 15+ | Logged, no automated outreach |

Reminders are sent via the configured email provider (Resend or SMTP) and tracked in the `reminder_logs` table to prevent duplicates.

**API endpoints:**

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/v1/engagement/status/{learner_id}` | Individual engagement status |
| `GET` | `/v1/engagement/summary` | Admin dashboard: attrition summary |
| `POST` | `/v1/engagement/send_reminder/{learner_id}` | Manually trigger a reminder |

---


## Post-Study Feature Unlock

After the study period ends, control-group learners (arms A and B) are granted access to the full feature set (explanations, sentiment panel, etc.) that was previously restricted to the treatment arm.

**Unlock conditions** (checked in order):

1. `PILOT_MODE=true`: immediate global unlock
2. Treatment arm (`T`): always has full features
3. `STUDY_END_DATE` has passed
4. `PILOT_START_DATE + STUDY_DURATION_WEEKS` has passed
5. Learner signup date + `STUDY_DURATION_WEEKS` has passed

**API endpoint:**

```bash
GET /v1/study/unlock/{learner_id}
```

Response includes `features_unlocked`, `study_ended`, `unlock_reason`, and `days_until_unlock`.

The `is_study_ended_for_learner()` utility function can be called from other routers (e.g., recommend, ARL) to conditionally override arm-based feature restrictions.

---


## Configuration Reference

| Variable | Default | Purpose | Notes |
| --- | --- | --- | --- |
| `DATABASE_URI` | `sqlite:///./data/xelra_app.db` | Primary app DB | Keep local for research runs. |
| `FEATURE_STORE_URI` | `sqlite:///./data/xelra_fs.db` | Feature store for ARL analytics | Keep separate from transactional DB. |
| `LOGIN_JWT_SECRET` | `change-me-login` | Signs learner tokens | Set a fixed secret to keep runs reproducible. |
| `LOGIN_TOKEN_TTL_MINUTES` | `43200` | TTL for login tokens (minutes) | Adjust per study length. |
| `LOGIN_JWT_LEEWAY_SECONDS` | `300` | Clock skew allowance | Keep default unless tests require tighter bounds. |
| `RESEND_API_KEY` | unset | Resend transactional email API key | Recommended for OTP and reminder emails. |
| `SMTP_*` | defaults | Outbound email for OTP login (legacy) | Fallback if Resend not configured. |
| `PILOT_MODE` | `false` | Enable all features for all arms | Use for end-of-study or pilot testing. |
| `SIGNUP_ENABLED` | `true` | Allow new user registration | When disabled, only existing users can sign in. |
| `DEMO_LEARNERS_ENABLED` | `true` | Allow @example.com demo accounts | Disable for production study runs. |
| `EXPLANATIONS`, `FEATURE_SENTIMENT`, `BASELINE`, `INFER_SENTIMENT` | `True` | Feature flags | Disable to gate endpoints/UI features. |
| `ENABLE_FORMAL_ARL` | `True` | Enable formal ARL controller | Activates explicit state tracking (S_t), mode inference, boundedness enforcement, and routine gating. |
| `SURVEY_ENABLED` | `True` | Enable periodic surveys | Surveys appear at configured week intervals. |
| `SURVEY_URL` | JISC URL | Survey form URL | Shown in an iframe; `?group=<arm>` is appended automatically. |
| `SURVEY_WEEKS` | `4,8,12` | Survey schedule | Comma-separated week numbers when surveys appear. |
| `PILOT_START_DATE` | unset | Study start date | `YYYY-MM-DD` format; uses learner signup date if not set. |
| `STUDY_END_DATE` | unset | Study end date | `YYYY-MM-DD` format. After this date, all features are unlocked for all arms. |
| `STUDY_DURATION_WEEKS` | `12` | Study duration in weeks | Used with `PILOT_START_DATE` (or learner signup) when `STUDY_END_DATE` is not set. |
| `HUGGING_FACE_HUB_TOKEN` | unset | Access private HF models | Required if sentiment inference stays on. |
| `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_WINDOW_SECONDS` | `600 / 60` | In-process rate limiting | Tune if you script high-volume tests. |

See `xelra/config.py` for full coverage of optional knobs.

---


## Privacy & Compliance

- **Consent gating:** `/v1/telemetry/consent` must return `consent_given=true` before impressions, clicks, or feedback are stored. Revocation purges recent sentiment aggregates.
- **Sentiment controls:** Set `INFER_SENTIMENT=0` and `FEATURE_SENTIMENT=0` to disable sentiment capture when you want a minimal telemetry footprint.

---


## Testing

This public-release archive includes the in-silico validation tests under `in-silico-experiments/tests/`.

```bash
cd in-silico-experiments
pytest tests
```

To run the full reproducibility suite (tests + all studies):

```bash
cd in-silico-experiments
python3 experiments/run_all.py
```

---