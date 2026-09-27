# X-ELRA

X-ELRA (eXplainable E-Learning Recommendation Architecture) is the reference implementation of Agentic Regulated Learning (ARL), developed for the PhD thesis *Agentic Regulated Learning: A Governance Architecture for Process-Level Explainability in Adaptive Learning Systems* (Simon West, University of Portsmouth).

This README covers installation, running, and reproduction only. The architecture, formal specification, terminology, study design, and results are described in the thesis, which is the authoritative reference for everything conceptual.

**Archive:** Zenodo, all versions: [10.5281/zenodo.21916376](https://doi.org/10.5281/zenodo.21916376). The thesis cites the specific version used.
**Licence:** MIT (see `LICENSE`)

---

## Contents

1. [Requirements](#requirements)
2. [Install](#install)
3. [Configure](#configure)
4. [Seed demo data](#seed-demo-data)
5. [Build lesson content](#build-lesson-content)
6. [Run the server](#run-the-server)
7. [Reproduce the simulation studies](#reproduce-the-simulation-studies)
8. [Repository layout](#repository-layout)
9. [Where the governance code lives](#where-the-governance-code-lives)
10. [Citation](#citation)

---

## Requirements

- Python 3.10 or later
- SQLite (included with Python)
- Optional: a Resend API key or SMTP account, for emailed login codes

## Install

```bash
pip install -r requirements.txt
```

## Configure

Settings are read from environment variables or a `.env` file in the repository root. No `.env` file is distributed; create one, or export the variables in your shell. A minimal local setup:

```bash
export DATABASE_URI="sqlite:///./data/xelra_app.db"
export FEATURE_STORE_URI="sqlite:///./data/xelra_fs.db"
export LOGIN_JWT_SECRET="replace-with-a-long-random-string"
```

Optional email for login codes (Resend is used if configured, otherwise SMTP):

```bash
export RESEND_API_KEY="..."
# or
export SMTP_HOST="smtp.example.com"
export SMTP_USER="username"
export SMTP_PASS="password"
export SMTP_FROM="noreply@example.com"
```

All settings, with their defaults, are defined in `xelra/config.py`.

## Seed demo data

```bash
python scripts/seed_demo_data.py
```

This **drops and recreates all tables**, then loads the PY101 course and eight demo learners (`@example.com` accounts). To seed without wiping existing data:

```bash
python scripts/seed_demo_data.py --no-reset
```

## Build lesson content

Lesson HTML is generated from the Markdown sources in `content/PY101/` and is not distributed. Build it once before serving lessons:

```bash
python scripts/build_content.py
```

## Run the server

```bash
uvicorn xelra.server.app:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- Web app: `http://localhost:8000/app/web/standalone.html`
- API documentation: `http://localhost:8000/docs`

To sign in as a demo learner, enter a demo email address and use the one-time code printed in the server log.

## Reproduce the simulation studies

The `in-silico-experiments/` directory contains the simulation studies, property-based tests, and bounded model checker reported in the thesis. See that directory's README for details.

```bash
cd in-silico-experiments
pip install -r requirements.txt
python3 experiments/run_all.py       # tests and all studies
python3 experiments/make_figures.py  # figures
```

Runs are seeded, so decision-level results are reproducible. The module checksums and seeds of the canonical run are recorded in the thesis (Appendix I).

## Repository layout

```
xelra/                  application package (server, governance engine,
                        open learner model, recommenders, telemetry)
config/                 routine configuration and experiment arm settings
content/PY101/          course source (Markdown)
static/                 web front end
scripts/                seeding, content build, server launcher
docs/                   API contract and optional extension notes
in-silico-experiments/  simulation studies and verification (own README)
data/                   created at runtime; not distributed
```

## Where the governance code lives

| Component | Location |
| --- | --- |
| Decision cycle | `xelra/arl/engine.py` |
| Controller state | `xelra/arl/controller_state.py` |
| Mode inference and transitions | `xelra/arl/mode_inference.py` |
| Budgets, cooldowns, stability checks | `xelra/arl/boundedness.py` |
| Routine configuration | `config/arl_routines.yaml` |
| Routine loading and evaluation | `xelra/arl/dsl.py`, `xelra/arl/routines.py`, `xelra/arl/conditions.py`, `xelra/arl/actions.py` |
| Decision record schema | `xelra/arl/schemas.py` |
| Learner-facing projection | `xelra/olm/regulatory.py` |
| Recommenders | `xelra/models/recommender/` |

## Citation

If you use this software, please cite the archived release:

> West, S. (2026). *X-ELRA: reference implementation of Agentic Regulated Learning* [Computer software]. Zenodo. https://doi.org/10.5281/zenodo.21916376
