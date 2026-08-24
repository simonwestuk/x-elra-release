# API Contract

## Recommendations API

`POST /v1/recommendations/by_group` accepts `learner_id`, `group` (`treatment`\|`control_a`\|`control_b`), `top_k`, and `explain_level`. The legacy `POST /v1/recommendations` endpoint remains for clients that need to specify `strategy` and `explain` flags explicitly. The `hybrid` strategy prefers the neural collaborative filtering model and falls back to the classical CF variant when necessary.

## Agentic Regulated Learning (ARL)

### Perception → Reasoning → Action → Evaluation loop

An ARL cycle ingests learner state, reasons over control routines, executes actions, and schedules follow-up evaluation.

1. **Perception** builds a `FeatureVector` snapshot for the learner by combining mastery, goal, impression, click, completion, and metadata streams before resolving the active control routine set and deterministic arm assignment.【F:xelra/arl/engine.py†L336-L358】【F:xelra/arl/schemas.py†L6-L62】
2. **Reasoning** seeds the cycle with a stable value derived from learner ID, bundle version, and feature timestamp; it evaluates enabled control routines and collects resulting recommendations and explanations.【F:xelra/arl/engine.py†L359-L379】【F:xelra/arl/schemas.py†L102-L160】
3. **Action** executes routine actions (logging telemetry, scheduling practice, surfacing explanations) and aggregates their telemetry payloads and learner-facing items.【F:xelra/arl/engine.py†L380-L399】【F:xelra/arl/actions.py†L28-L463】
4. **Evaluation** snapshots the outcome, computes a deterministic hash for replay, persists the decision, and enqueues an `EvaluationJob` enriched with telemetry metadata.【F:xelra/arl/engine.py†L400-L447】【F:xelra/arl/schemas.py†L162-L199】

#### Control routine catalogue (P1–P8)

| Routine | Priority | Conditions (all) | Actions |
| --- | --- | --- | --- |
| **P1 Orientation safety net** | 120 | No mastery data; no impressions in the last 30 days; no existing arm assignment.【F:config/arl_routines.yaml†L1-L31】 | Fetch the orientation playlist (sequence, top 5) and log impressions to `arl_orientation` telemetry.【F:config/arl_routines.yaml†L18-L27】 |
| **P2 Data integrity** | 110 | Feature gap detected; mastery missing or incomplete.【F:config/arl_routines.yaml†L32-L56】 | Fetch a hybrid diagnostics bundle (top 5, diagnostics enabled) and log it to `arl_diagnostics` telemetry.【F:config/arl_routines.yaml†L42-L51】 |
| **P8 Affective overload intervention** | 95 | Frustration or confusion detected (affect flags from live code errors + sentiment).【F:config/arl_routines.yaml†L83-L125】 | Suggest a wellbeing break (5 min microbreak) and fetch a short fundamentals reset (content, top 3), logged to `arl_affect` telemetry.【F:config/arl_routines.yaml†L96-L115】 |
| **P3 Struggling learner uplift** | 90 | Lowest mastery under 0.4; no clicks in the last 14 days.【F:config/arl_routines.yaml†L57-L81】 | Fetch a fundamentals-focused content refresh and log to `arl_foundations` telemetry.【F:config/arl_routines.yaml†L65-L74】 |
| **P4 Lapsed learner re-engagement** | 80 | Last impression over 30 days ago; learner still has goals.【F:config/arl_routines.yaml†L82-L108】 | Fetch a goal-emphasising hybrid set and log to `arl_reengagement` telemetry.【F:config/arl_routines.yaml†L90-L99】 |
| **P5 Goal attainment accelerator** | 70 | Active goals exist; progress rate ≥ 0.05.【F:config/arl_routines.yaml†L109-L134】 | Fetch a goal-boosted hybrid accelerator and log to `arl_goalpath` telemetry.【F:config/arl_routines.yaml†L117-L126】 |
| **P6 Mastery consolidation** | 60 | Highest mastery ≥ 0.85; at least one completion in the last 7 days.【F:config/arl_routines.yaml†L135-L162】 | Fetch consolidation drills that diversify practice and log to `arl_consolidation` telemetry.【F:config/arl_routines.yaml†L143-L152】 |
| **P7 Default hybrid pathway** | 10 | No other routine triggered (empty condition set).【F:config/arl_routines.yaml†L215-L242】 | Fetch the default hybrid set and log to `arl_default` telemetry.【F:config/arl_routines.yaml†L222-L231】 |

> **Priority resolution.** Higher numeric `priority` values run first. Lower-priority routines (such as P7) execute only when earlier control routines do not fire.【F:config/arl_routines.yaml†L8-L178】

### Public ARL APIs

All public ARL endpoints live under the `/v1` prefix and require a Bearer token validated via `verify_login_token`.

#### `POST /v1/arl`

*Request body.* `ARLRequest` accepts optional `learner_id`, `routine_path`, `refresh_features`, `override_arm`, and `verify_assignment` flags.【F:xelra/routers/api.py†L30-L63】

*Response.* `ARLCycleResponse` returns the learner ID, `decision_id`, `deterministic_hash`, routine version, cycle `seed`, feature snapshot, per-routine results, explanations, telemetry events, optional `evaluation_job`, and optional replay check metadata.【F:xxelra/routers/api.py†L64-L128】

*Use cases.* Invoke this endpoint to run an on-demand cycle. Supplying `override_arm` forces a new arm assignment before the cycle completes.【F:xelra/routers/api.py†L129-L197】

#### `POST /v1/arl/event`

*Request body.* `ARLEventRequest` adds `event_type`, optional metadata, and optional `refresh_features`. When omitted, refresh defaults to true for `error`, `baseline`, or `time` triggers.【F:xelra/routers/api.py†L42-L88】【F:xelra/routers/api.py†L199-L225】

*Response.* Same as `/v1/arl`, with an additional telemetry record noting the event trigger and metadata.【F:xelra/routers/apipy†L171-L188】【F:xxelra/routers/api.py†L205-L225】

#### `POST /v1/arl/trigger`

Identical to `/v1/arl` but intended for system-driven triggers (e.g., scheduler hooks) without the automatic event telemetry envelope.【F:xxelra/routers/api.py†L226-L244】

#### `POST /v1/arl/override`

*Request body.* `ArmOverrideRequest` requires `arm` and accepts an optional `learner_id` (defaulting to the token subject).【F:xelra/routers/api.py†L246-L259】

*Response.* Returns the effective learner ID, arm, and override status via `ArmOverrideResponse`. The handler normalises the arm slug to uppercase and persists it immediately.【F:xelra/routers/api.py†L260-L279】

### Admin ARL APIs

All admin endpoints require an admin principal (`require_admin`) and are namespaced under `/v1/admin`.

#### `POST /v1/admin/arl`

*Request body.* `AdminARLRequest` exposes toggles for running a cycle, overriding an arm, verifying deterministic replay, reloading control routines, refreshing features, and pointing to an alternate routine bundle.【F:xelra/routers/admin_arl.py†L28-L65】

*Response.* `AdminARLResponse` combines optional `cycle`, `replay`, `override`, and `routine` payloads depending on which toggles were set. Cycle payloads mirror `ARLCycleResponse` minus the replay metadata envelope.【F:xelra/routers/admin_arl.py†L67-L152】

*Notes.* When `run_cycle` is true, the service persists telemetry and, if necessary, schedules replay verification after assigning a new arm.【F:xelra/routers/admin_arl.py†L153-L196】

#### `POST /v1/admin/arl/replay`

Returns deterministic arm status (`match`, `mismatch`, `not_assigned`) for a learner without executing a cycle.【F:xelra/routers/admin_arl.py†L198-L228】

#### `POST /v1/admin/arl/reload`

Reloads the control routine bundle (optionally from a supplied path) and responds with the new version, schema version, and routine count.【F:xelra/routers/admin_arl.py†L230-L261】

### Determinism, seeds, and telemetry artifacts

* `deterministic_hash` is a SHA-256 digest of the canonicalised cycle snapshot (routine outputs plus seed). It guarantees that identical learner context and routine bundle reproduce the same hash, enabling replay checks and audit joins.【F:xelra/arl/engine.py†L371-L409】
* `seed` is derived from learner ID, routine bundle version, and feature timestamp. Control routines and actions use it to produce stable pseudo-random choices across replays.【F:xelra/arl/engine.py†L344-L378】【F:xelra/arl/schemas.py†L102-L138】
* `telemetry_events` aggregate payloads emitted by routine actions (`telemetry` entries in action payloads) and optional trigger annotations so downstream pipelines can reason about what the cycle attempted.【F:xelra/arl/actions.py†L28-L463】【F:xelra/routers/api.py†L171-L188】
* `evaluation_job` describes deferred validation work (job ID, affected routines, trigger metadata) scheduled alongside the decision.【F:xelra/arl/engine.py†L410-L447】【F:xelra/arl/schemas.py†L140-L199】

### Telemetry arm replay

`POST /v1/telemetry/arm/replay` replays deterministic arm assignments for a batch of learners. The request body contains `learner_ids` (array of IDs), and the response includes the active arms manifest snapshot plus per-learner assignments with resolved bucket, arm slug, and configuration (weights, sentiment settings, routine version).【F:xelra/server/routers/telemetry.py†L360-L470】

```bash
curl -X POST "https://api.example.org/v1/telemetry/arm/replay" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
        "learner_ids": ["learner-alpha", "learner-beta"]
      }'
```

Interpret the response as follows:

* `manifest` mirrors the `config/arms.yaml` file at request time, enabling snapshot comparisons during investigations.【F:xelra/server/routers/telemetry.py†L404-L453】
* `assignments[].bucket` is the deterministic bucket, while `assignments[].arm` resolves to the arm slug configured for that bucket.【F:xelra/server/routers/telemetry.py†L432-L458】
* `assignments[].config` captures strategy settings, routine version, recommender weight map, and sentiment controls for that arm.【F:xelra/server/routers/telemetry.py†L444-L465】

#### Outcome windows and replay analysis

Control routine conditions often use helper pipelines such as `last_14_days` or `last_30_days`, which count timestamped events within the specified sliding window when evaluating feature history. These helpers normalise timestamps to UTC and only increment counts for entries newer than the cutoff, ensuring replayed cycles reflect recent engagement accurately.【F:xelra/arl/conditions.py†L64-L121】

During investigations, compare telemetry replay outputs with ARL cycle responses: matching `deterministic_hash` values confirm that the same feature snapshot and seed drove both the learner-facing action plan and the telemetry replay evidence.【F:xelra/arl/engine.py†L371-L447】
POST ``/v1/recommend/recommendations/by_group`` with fields matching ``GroupRecRequest``:

- ``learner_id`` – UUID/slug for the learner (required)
- ``group`` – ``treatment`` | ``control_a`` | ``control_b`` (required)
- ``context`` – optional object (``course_id``, ``time``) mirroring the standard recommendation context
- ``top_k`` – maximum recommendations to return (defaults to 10)
- ``explain_level`` – ``short`` | ``detailed`` | ``auto`` (defaults to ``auto``)

The original ``/v1/recommend/recommendations`` endpoint remains available for clients that wish to explicitly specify ``strategy`` and ``explain`` flags. Prefer calling ``ExperimentGroup.to_request`` to generate those legacy payloads so the helper and documentation stay in sync. Older clients may continue using the legacy path, but new integrations should migrate to ``/v1/recommend/recommendations/by_group``.
## Recommendation group helper

`POST /v1/recommend/recommendations/by_group`

- **Purpose:** Resolve an experiment group to the appropriate recommender strategy and explanation flag.
- **Required fields:** `learner_id`, `group` (`treatment`|`control_a`|`control_b`), `top_k` (int), optional `explain_level`.
- **Notes:** The legacy `/v1/recommend/recommendations` endpoint remains available when clients need to set `strategy` and `explain` manually.
- **Sample response:**
  ```json
  {
    "learner_id": "alice",
    "recommendations": [
      {"item_id": "intro-python", "rank": 1, "score": 0.91}
    ],
    "arm": "control_a",
    "routine_version": "2025.04",
    "explain": false
  }
  ```

---

## Telemetry endpoints

### `POST /v1/telemetry/completion`
- **Purpose:** Persist an explicit completion and trigger mastery updates.
- **Required fields:** `learner_id`, `item_id`, `user_id`, `arm_key`, `routine_version`, `schema_version`. Optional `source`, `rank`, `strategy`, `course_id`, `request_id`.
- **Sample response:**
  ```json
  {"ok": true}
  ```

### `POST /v1/telemetry/reflection`
- **Purpose:** Store a learner reflection with optional topic, prompt, sentiment override, and metadata blob.
- **Required fields:** `learner_id`, `text`, `user_id`, `arm_key`, `routine_version`, `schema_version`. Optional `topic`, `item_id`, `prompt`, `sentiment`, `metadata`.
- **Sample response:**
  ```json
  {"ok": true, "reflection_id": 4812}
  ```

### `POST /v1/telemetry/live/{event}`
- **Purpose:** Record live-code iframe activity (impressions, run lifecycle, hints, reflections, ARL nudges) emitted directly by lesson frames.
- **Supported events:** `impression`, `run`, `success`, `hint`, `reflection`, `arl_nudge`.
- **Required fields:** `learner_id` (when known) plus event-specific payload such as `cell_id`, `status`, `duration_ms`, `output_preview`, `error_type`, `response`, or `message`. The request body may include a `metadata` object for arbitrary structured context.
- **Sample request:**
  ```json
  {
    "event": "run",
    "learner_id": "learner-123",
    "item_id": "lesson-debugging",
    "cell_id": "cell-2",
    "engine": "pyodide",
    "status": "success",
    "duration_ms": 940,
    "output_preview": "Finished in 0.94s",
    "metadata": {"lesson_url": "https://lms.example.org/lesson/123"}
  }
  ```
- **Sample response:**
  ```json
  {"ok": true, "event": "run", "id": 27}
  ```

### `POST /v1/telemetry/gdpr_delete`
- **Purpose:** Delete the learner record and purge cached sentiment artefacts after consent is withdrawn.
- **Auth:** Basic admin credentials (`Authorization: Basic …`).
- **Required fields:** `learner_id`.
- **Sample response:**
  ```json
  {"ok": true, "learner_id": "learner-123", "purged": {"sentiment_scores": 5}}
  ```

### `POST /v1/telemetry/arm/replay`
- **Purpose:** Replay deterministic bucket assignments and return the manifest snapshot for compliance checks.
- **Required fields:** `learner_ids` (array of learner IDs).
- **Sample response:**
  ```json
  {
    "manifest": {
      "routine": {"version": "2025.04"},
      "buckets": {"T": "treatment", "A": "control_a", "B": "control_b"},
      "weights": {"treatment": 0.334, "control_a": 0.333, "control_b": 0.333},
      "arms": {"treatment": {"label": "Governed adaptive system with structured explanations"}}
    },
    "assignments": [
      {
        "learner_id": "learner-123",
        "bucket": "T",
        "arm": "treatment",
        "config": {
          "label": "Governed adaptive system with structured explanations",
          "strategy": "hybrid",
          "explain": true,
          "routine_version": "v2",
          "weight_map": {"content": 0.45, "cf": 0.25, "popularity": 0.1, "sentiment": 0.2},
          "sentiment": {"enabled": true, "provider": "huggingface", "model": "distilbert-base-uncased-finetuned-sst-2-english"}
        }
      }
    ]
  }
  ```

---

## Feedback and sentiment endpoints

### `GET /v1/feedback/latest_explain/{learner_id}`
- **Purpose:** Retrieve the latest reflection with stored sentiment scores and token-level XAI weights.
- **Required path params:** `learner_id`.
- **Sample response:**
  ```json
  {
    "ok": true,
    "text": "I finally understand decorators!",
    "polarity": 0.82,
    "confidence": 0.91,
    "lime": {"tokens": ["I", "finally", "understand", "decorators"], "weightsPos": [[2, 0.3]], "weightsNeg": []},
    "shap": {"tokens": [], "weightsPos": [], "weightsNeg": []}
  }
  ```

### `POST /v1/sentiment/explain`
- **Purpose:** Produce HTML, token, and weight explainers for an arbitrary text snippet.
- **Required fields:** `text`.
- **Sample response:**
  ```json
  {
    "ok": true,
    "html": "<div class=\"sentiment-explain\">…</div>",
    "tokens": ["great", "course"],
    "weightsPos": [[0, 0.45]],
    "weightsNeg": []
  }
  ```

### `POST /v1/sentiment/batch`
- **Purpose:** Score multiple reflections, persisting/updating rows and returning the model judgments.
- **Required fields:** `reflections` (array of `{learner_id, text}`); each payload may also include `topic`, `item_id`, `prompt`, `metadata`, and `id` to upsert an existing reflection.
- **Sample response:**
  ```json
  {
    "results": [
      {
        "reflection_id": 930,
        "learner_id": "learner-001",
        "topic": "Python",
        "label": "POSITIVE",
        "confidence": 0.88,
        "polarity": 0.74
      }
    ]
  }
  ```

---

## Adaptive Recommendation Loop (ARL)

### `POST /v1/arl`
- **Purpose:** Run an ARL cycle for the learner identified in the bearer token.
- **Required fields:** `learner_id` (falls back to token subject when omitted), optional `routine_path`, `refresh_features`.
- **Sample response:**
  ```json
  {
    "cycle": {
      "arm": "treatment",
      "recommendations": [
        {"item_id": "intro-python", "rank": 1, "reason": "low mastery"}
      ]
    },
    "telemetry_events": [
      {"type": "impression", "items": ["intro-python"]}
    ]
  }
  ```

### `POST /v1/arl/event`
- **Purpose:** Map an external trigger (e.g., `baseline`, `time`, `error`) to an ARL cycle and log the trigger metadata.
- **Required fields:** `learner_id`, `event_type`; optional `routine_path`, `refresh_features`, `metadata`.
- **Sample response:**
  ```json
  {
    "cycle": {"arm": "treatment", "recommendations": []},
    "telemetry_events": [
      {"type": "trigger", "trigger": "baseline", "metadata": {"source": "cron"}}
    ],
    "replay": null
  }
  ```

### `POST /v1/arl/trigger`
- **Purpose:** Force an ARL cycle without event metadata decoration.
- **Required fields:** Same as `POST /v1/arl`.
- **Sample response:**
  ```json
  {
    "cycle": {"arm": "control_a", "recommendations": []},
    "telemetry_events": []
  }
  ```

### `POST /v1/arl/override`
- **Purpose:** Override the learner's arm assignment (admin token required).
- **Required fields:** `arm`; optional `learner_id` (defaults to token subject).
- **Sample response:**
  ```json
  {"learner_id": "learner-123", "arm": "B", "status": "overridden"}
  ```

### `POST /v1/arl/replay`
- **Purpose:** Verify deterministic arm assignment against the stored record (admin auth enforced).
- **Required fields:** `learner_id`.
- **Sample response:**
  ```json
  {
    "learner_id": "learner-123",
    "expected_arm": "B",
    "stored_arm": "B",
    "status": "match"
  }
  ```

### `POST /v1/arl/reload`
- **Purpose:** Reload the ARL control routine bundle and expose the resulting version metadata (admin auth enforced).
- **Required fields:** `routine_path`.
- **Sample response:**
  ```json
  {
    "version": "2025.05",
    "schema_version": "1.1",
    "routine_count": 6
  }
  ```

---

## Compliance and access controls

- Learner telemetry that captures identifiable data must only be recorded when consent is granted via `POST /v1/telemetry/consent`; callers should poll `GET /v1/telemetry/consent/{learner_id}` before logging reflections or sentiment.
- Admin-only workflows require Basic authentication (telemetry GDPR delete) or admin bearer tokens (ARL override/replay/reload). Coordinate with security operations before enabling these routes in production.
- GDPR deletion and ARL replay verification workflows are documented in the sections above: see [`POST /v1/telemetry/gdpr_delete`](#post-v1telemetrygdpr_delete) and [`POST /v1/arl/replay`](#post-v1arlreplay) for payloads and responses.
