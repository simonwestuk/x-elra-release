"""Seed and reset demo data for local/dev X-ELRA environments."""

import argparse
import datetime as dt
import json
import os
import re
from typing import List, Tuple
import uuid  # Use GUIDs for learner_id in seed data

from xelra.utils.db import (
    SessionLocal,
    Base,
    engine,
    init_db,
    LearnerConsent,
    GroupAssignment,
    Impression,
    Click,
    ExplanationInteraction,
    Item,
    LearnerPreference,
    Skill,
    ItemSkill,
    Mastery,
    Goal,
    User,
    Feedback,
    SentimentScore,
    ItemSentimentAgg,
    LearnerSentimentWindow,
    Completion,
    MasteryEvidence,
    ARLDecision,
    ARLOutcome,
    SentimentAggregate,
    Reflection,
    OLMEvent,
)

"""
Seed data for PY101 Python Fundamentals course.

This seed respects the three-group design (T, A, B) and demonstrates all
controller modes and control routines for the Agentic Regulated Learning (ARL)
system.

Groups:
- T (Treatment): Governed adaptive system with process-level regulatory explanations and
  learner-facing progress projections.
- A (Control A): Model-driven adaptive system with basic model-level
  explanations.
- B (Control B): System displaying learner progress information without
  structured explanations of decision processes.

Controller Modes demonstrated:
- COLD_START: New learner, no telemetry (frank@example.com)
- ORIENTATION: Initial onboarding, early engagement (olivia@example.com)
- NOMINAL: Steady-state learning (notag@example.com)
- STRUGGLING: Requires intervention (bob@example.com)
- LAPSED: Re-engagement needed (carol@example.com)
- ACCELERATING: High momentum (dave@example.com)
- CONSOLIDATING: Mastery reinforcement (eve@example.com)
- DIAGNOSTIC: Data integrity check (alice@example.com)

Control Routines demonstrated:
- P1: Orientation Safety Net (frank@, olivia@)
- P2: Data Integrity Control Routine (alice@)
- P3: Struggling Learner Uplift (bob@)
- P4: Lapsed Learner Re-engagement (carol@)
- P5: Goal Attainment Accelerator (dave@)
- P6: Mastery Consolidation (eve@)
- P7: Default Hybrid Pathway (notag@)
"""

PY101_COURSE_ID = "PY101"


def _is_production():
    """Check if the current environment looks like production."""
    env = os.environ.get("ENVIRONMENT", "").lower()
    return env in ("production", "prod")


def reset_db():
    """Drop and recreate all tables.

    Refuses to run in production unless SEED_FORCE=1 is set, to prevent
    accidental data loss.
    """
    if _is_production() and not os.environ.get("SEED_FORCE", "").lower() in ("1", "true", "yes"):
        raise RuntimeError(
            "Refusing to drop all tables: ENVIRONMENT is set to production. "
            "If you really mean it, set SEED_FORCE=1."
        )
    Base.metadata.drop_all(bind=engine)
    init_db()


# ------------------------------------------------------------
# PY101 Skills - one per module, levels 1-7
# These form the progressive skill tree for Python Fundamentals
# ------------------------------------------------------------
PY101_SKILLS_DEF: List[Tuple[str, str, int]] = [
    ("py101-foundations", "Python Foundations", 1),
    ("py101-control-flow", "Control Flow", 2),
    ("py101-data-structures", "Data Structures", 3),
    ("py101-functions", "Functions", 4),
    ("py101-error-handling", "Error Handling", 5),
    ("py101-file-ops", "File Operations", 6),
    ("py101-building-apps", "Building Applications", 7),
]

# ------------------------------------------------------------
# PY101 Module -> Topics -> Content Items
# Each topic has 4 types: lesson, practice, challenge, reference
# Total: 7 modules, 48 topics, 192 resources
# ------------------------------------------------------------
PY101_MODULES = {
    "python-foundations": {
        "skill_id": "py101-foundations",
        "module_order": 1,
        "topics": [
            "print-basics",
            "comments",
            "variables-types",
            "numbers-math",
            "strings",
            "string-methods",
            "string-formatting",
            "user-input",
        ],
    },
    "control-flow": {
        "skill_id": "py101-control-flow",
        "module_order": 2,
        "topics": [
            "comparisons",
            "booleans",
            "if-statements",
            "else-elif",
            "logical-operators",
            "nested-conditions",
            "while-loops",
            "for-loops",
            "loop-control",
            "nested-loops",
        ],
    },
    "data-structures": {
        "skill_id": "py101-data-structures",
        "module_order": 3,
        "topics": [
            "lists",
            "list-operations",
            "slicing",
            "list-iteration",
            "comprehensions",
            "tuples",
            "dicts",
            "dict-operations",
        ],
    },
    "functions": {
        "skill_id": "py101-functions",
        "module_order": 4,
        "topics": [
            "defining-functions",
            "parameters",
            "return-values",
            "defaults",
            "scope",
            "docstrings",
        ],
    },
    "error-handling": {
        "skill_id": "py101-error-handling",
        "module_order": 5,
        "topics": [
            "syntax-errors",
            "exceptions",
            "try-except",
            "raising-errors",
            "debugging",
        ],
    },
    "file-operations": {
        "skill_id": "py101-file-ops",
        "module_order": 6,
        "topics": [
            "reading-files",
            "writing-files",
            "file-modes",
            "context-managers",
            "csv-data",
        ],
    },
    "building-apps": {
        "skill_id": "py101-building-apps",
        "module_order": 7,
        "topics": [
            "program-structure",
            "modules-imports",
            "input-validation",
            "state-management",
            "refactoring",
            "capstone-prep",
        ],
    },
}

RESOURCE_TYPES = [
    ("lesson", "Lesson", 12),
    ("practice", "Practice", 15),
    ("challenge", "Challenge", 20),
    ("reference", "Reference", 3),
]


def _pop(module_order: int, topic_idx: int) -> float:
    """Calculate popularity score based on module and topic position."""
    base = 0.95 - (module_order * 0.06) - (topic_idx * 0.02)
    return round(max(base, 0.3), 2)


def _dur(res_type: str, topic_idx: int) -> int:
    """Calculate duration based on resource type and complexity."""
    base_durations = {"lesson": 12, "practice": 15, "challenge": 20, "reference": 3}
    base = base_durations.get(res_type, 10)
    return base + (topic_idx // 3)


def _build_items() -> Tuple[List[Item], dict]:
    """Build the list of Item objects and skill mappings without persisting them."""
    items: List[Item] = []
    mapping = {}  # item_id -> list[(skill_id, weight)]

    item_counter = 0
    for module_name, module_data in PY101_MODULES.items():
        skill_id = module_data["skill_id"]
        module_order = module_data["module_order"]

        for topic_idx, topic in enumerate(module_data["topics"], start=1):
            for res_type, res_label, _ in RESOURCE_TYPES:
                item_counter += 1
                item_id = f"py101_{item_counter:04d}"
                topic_title = topic.replace("-", " ").title()

                if res_type == "lesson":
                    title = f"{topic_title}"
                elif res_type == "practice":
                    title = f"Practice: {topic_title}"
                elif res_type == "challenge":
                    title = f"Challenge: {topic_title}"
                else:
                    title = f"Quick Reference: {topic_title}"

                slug = f"{topic}-{res_type}"
                url = f"/content/PY101/{module_name}/{slug}.html"

                item = Item(
                    item_id=item_id,
                    title=title,
                    topics=f"python,{module_name},{topic}",
                    popularity=_pop(module_order, topic_idx),
                    url=url,
                    course_id=PY101_COURSE_ID,
                    type=res_type,
                    duration_mins=_dur(res_type, topic_idx),
                )
                items.append(item)
                mapping[item_id] = [(skill_id, 1.0)]

    return items, mapping


def seed_learning_materials():
    """Seed skills, items, and item-skill mappings if they don't already exist.

    This is safe to call on every startup — it only inserts data when the
    items table is empty, so it won't duplicate rows.
    """
    init_db()
    db = SessionLocal()
    try:
        existing_items = db.query(Item).first()
        if existing_items is not None:
            print("[seed] Learning materials already present — skipping.")
            return

        print("[seed] Seeding learning materials (skills, items, item-skill mappings)...")

        # Skills
        skills = [
            Skill(id=sid, name=name, level=level)
            for sid, name, level in PY101_SKILLS_DEF
        ]
        db.add_all(skills)

        # Items and item-skill mappings
        items, mapping = _build_items()
        db.add_all(items)
        for item_id, arr in mapping.items():
            for skill_id, weight in arr:
                db.add(ItemSkill(item_id=item_id, skill_id=skill_id, weight=weight))

        db.commit()
        print(f"[seed] Seeded {len(items)} learning items and {len(skills)} skills.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def seed(*, reset: bool = True):
    if reset:
        reset_db()
    else:
        init_db()  # create tables if they don't exist, but keep data
    db = SessionLocal()
    routine_version = "pv-py101"
    schema_version = "arl/v2"
    now = dt.datetime.now(dt.timezone.utc)

    def ts_days_ago(days: int) -> dt.datetime:
        return now - dt.timedelta(days=days)

    py101_skills_def = PY101_SKILLS_DEF

    skills = [
        Skill(id=sid, name=name, level=level)
        for sid, name, level in py101_skills_def
    ]
    db.add_all(skills)

    items, mapping = _build_items()
    db.add_all(items)

    # Map items to skills
    for item_id, arr in mapping.items():
        for skill_id, weight in arr:
            db.add(ItemSkill(item_id=item_id, skill_id=skill_id, weight=weight))

    # ------------------------------------------------------------
    # Demo Learners - Each demonstrates a specific controller mode
    # and control routine for the ARL system
    #
    # Three-group design:
    #   T = Treatment (governed adaptive + structured explanations)
    #   A = Control A (model-driven adaptive + basic explanations)
    #   B = Control B (progress display, no structured explanations)
    # ------------------------------------------------------------
    all_skill_ids = [sid for sid, _, _ in py101_skills_def]

    learners = [
        # ============================================================
        # P1: ORIENTATION SAFETY NET (COLD_START mode)
        # Entry: Empty mastery + 0 impressions in 30 days
        # ============================================================
        {
            "scenario": "P1 — Orientation safety net (cold start)",
            "email": "frank@example.com",
            "arm": "T",
            "pref": "auto",
            "mastery": [],  # Empty mastery triggers COLD_START
            "goals": [],
            "impressions": [],  # No impressions
            "clicks": [],
            "completions": [],
            "explanations": [],
            "feedback": [],
            "reflections": [],
            "olm_events": [],
            "sentiment_topics": [],
            "baseline": {
                "results": {},
                "scores": {},
                "mastery_init": {},
                "srl_profile": {"planning": 0.0, "monitoring": 0.0, "reflection": 0.0},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0001", "score": 1.0},
                    {"item_id": "py101_0002", "score": 0.99},
                    {"item_id": "py101_0005", "score": 0.98},
                ],
                "days_ago": 0,
            },
        },
        # ============================================================
        # P1: ORIENTATION (early engagement, 1-9 impressions)
        # Entry: Empty mastery + 1-9 impressions (early engagement)
        # ============================================================
        {
            "scenario": "P1 — Orientation (early engagement)",
            "email": "olivia@example.com",
            "arm": "T",
            "pref": "auto",
            "mastery": [],  # Still empty mastery
            "goals": [],
            "impressions": [
                # 3 impressions - triggers ORIENTATION mode
                {
                    "item_id": "py101_0001",
                    "strategy": "hybrid",
                    "explain_level": "auto",
                    "score": 0.95,
                    "source": "recs",
                    "days_ago": 2,
                },
                {
                    "item_id": "py101_0002",
                    "strategy": "hybrid",
                    "explain_level": "auto",
                    "score": 0.92,
                    "source": "recs",
                    "days_ago": 1,
                },
                {
                    "item_id": "py101_0005",
                    "strategy": "hybrid",
                    "explain_level": "auto",
                    "score": 0.88,
                    "source": "recs",
                    "days_ago": 0,
                },
            ],
            "clicks": [
                {
                    "item_id": "py101_0001",
                    "action": "click",
                    "source": "recs",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "T",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 2,
                },
            ],
            "completions": [],
            "explanations": [],
            "feedback": [],
            "reflections": [
                {
                    "topic": "py101-foundations",
                    "item_id": "py101_0001",
                    "text": "Just starting out with Python. The print() function is cool!",
                    "sentiment": 0.7,
                    "days_ago": 2,
                }
            ],
            "olm_events": [],
            "sentiment_topics": [],
            "baseline": {
                "results": {"py101-foundations": "discover"},
                "scores": {"py101-foundations": 0.15},
                "mastery_init": {"py101-foundations": 0.1},
                "srl_profile": {"planning": 0.25, "monitoring": 0.2, "reflection": 0.15},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0005", "score": 0.95},
                    {"item_id": "py101_0009", "score": 0.92},
                    {"item_id": "py101_0013", "score": 0.88},
                ],
                "days_ago": 0,
            },
        },
        # ============================================================
        # P2: DATA INTEGRITY CONTROL ROUTINE (DIAGNOSTIC mode)
        # Entry: Feature gap > 2 (multiple missing data sources)
        # Must NOT trigger COLD_START/ORIENTATION first (needs mastery)
        # ============================================================
        {
            "scenario": "P2 — Data integrity control routine",
            "email": "alice@example.com",
            "arm": "A",
            "pref": "auto",
            "mastery": [("py101-foundations", 0.55)],  # Has mastery to avoid COLD_START/ORIENTATION
            "goals": [],  # No goals set (missing data) → feature_gap +1
            "impressions": [],  # No impressions (missing data) → feature_gap +1
            "clicks": [],  # No clicks (missing data) → feature_gap +1
            "completions": [],  # No completions (missing telemetry) → feature_gap +1
            # Total feature_gap = 4 > 2, triggers DIAGNOSTIC
            "explanations": [],  # No explanations (missing data)
            "feedback": [],  # No feedback (missing data)
            "reflections": [],  # No reflections (missing data)
            "olm_events": [],
            "sentiment_topics": [],  # No sentiment data (missing data)
            "baseline": {
                "results": {"py101-foundations": "reinforce"},
                "scores": {"py101-foundations": 0.62},
                "mastery_init": {"py101-foundations": 0.5},
                "srl_profile": {"planning": 0.55, "monitoring": 0.48, "reflection": 0.42},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0013", "score": 0.82},
                    {"item_id": "py101_0017", "score": 0.78},
                    {"item_id": "py101_0021", "score": 0.72},
                ],
                "days_ago": 1,
            },
        },
        # ============================================================
        # P3: STRUGGLING LEARNER UPLIFT (STRUGGLING mode)
        # Entry: Lowest mastery < 0.4, no clicks in 14 days, impressions > 5
        # ============================================================
        {
            "scenario": "P3 — Struggling learner uplift",
            "email": "bob@example.com",
            "arm": "A",
            "pref": "auto",
            "mastery": [
                ("py101-foundations", 0.85),
                ("py101-control-flow", 0.25),  # Lowest mastery < 0.4 triggers STRUGGLING
            ],
            "goals": [],
            "impressions": [
                # 6 impressions within last 30 days (impressions_30d > 5)
                # But last click > 14 days ago (clicks_14d == 0) - learner saw recs but didn't engage
                {"item_id": "py101_0033", "strategy": "hybrid", "explain_level": "auto", "score": 0.74, "source": "recs", "days_ago": 5},
                {"item_id": "py101_0037", "strategy": "hybrid", "explain_level": "auto", "score": 0.72, "source": "recs", "days_ago": 10},
                {"item_id": "py101_0041", "strategy": "hybrid", "explain_level": "auto", "score": 0.70, "source": "recs", "days_ago": 15},
                {"item_id": "py101_0045", "strategy": "hybrid", "explain_level": "auto", "score": 0.68, "source": "recs", "days_ago": 18},
                {"item_id": "py101_0049", "strategy": "hybrid", "explain_level": "auto", "score": 0.66, "source": "recs", "days_ago": 22},
                {"item_id": "py101_0053", "strategy": "hybrid", "explain_level": "auto", "score": 0.64, "source": "recs", "days_ago": 28},
            ],
            "clicks": [
                # Last click > 14 days ago (clicks_14d == 0)
                {
                    "item_id": "py101_0033",
                    "action": "click",
                    "source": "recs",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "A",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 35,
                }
            ],
            "completions": [
                {
                    "item_id": "py101_0033",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "A",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 35,
                }
            ],
            "explanations": [],
            "feedback": [],
            "reflections": [
                {
                    "topic": "py101-control-flow",
                    "item_id": "py101_0037",
                    "text": "Loops are confusing. I keep getting infinite loops.",
                    "sentiment": -0.35,
                    "days_ago": 34,
                }
            ],
            "olm_events": [],
            "sentiment_topics": [
                {
                    "topic": "control_flow_frustration",
                    "mean": -0.25,
                    "slope": -0.02,
                    "intercept": -0.15,
                    "samples": 4,
                    "days_ago": 30,
                }
            ],
            "baseline": {
                "results": {"py101-control-flow": "strengthen"},
                "scores": {"py101-control-flow": 0.3},
                "mastery_init": {"py101-control-flow": 0.2},
                "srl_profile": {"planning": 0.45, "monitoring": 0.38, "reflection": 0.32},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0037", "score": 0.75},
                    {"item_id": "py101_0041", "score": 0.72},
                    {"item_id": "py101_0045", "score": 0.68},
                ],
                "days_ago": 0,
            },
        },
        # ============================================================
        # P4: LAPSED LEARNER RE-ENGAGEMENT (LAPSED mode)
        # Entry: >15 days since last engagement, active goals (Table 4)
        # ============================================================
        {
            "scenario": "P4 — Lapsed learner re-engagement",
            "email": "carol@example.com",
            "arm": "B",
            "pref": "detailed",
            "mastery": [
                ("py101-foundations", 1.0),
                ("py101-control-flow", 0.65),
                ("py101-data-structures", 0.50),
            ],
            "goals": [("py101-data-structures", 0.75)],  # Active goal required for LAPSED
            "impressions": [
                {
                    "item_id": "py101_0073",
                    "strategy": "hybrid",
                    "explain_level": "detailed",
                    "score": 0.73,
                    "source": "recs",
                    "days_ago": 20,  # >15 days ago (lapsed per Table 4)
                }
            ],
            "clicks": [
                {
                    "item_id": "py101_0073",
                    "action": "click",
                    "source": "recs",
                    "rank": 2,
                    "strategy": "hybrid",
                    "arm": "B",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 20,  # >15 days ago (lapsed per Table 4)
                }
            ],
            "completions": [
                {
                    "item_id": "py101_0069",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "B",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 22,
                }
            ],
            "explanations": [],
            "feedback": [],
            "reflections": [
                {
                    "topic": "py101-data-structures",
                    "item_id": "py101_0073",
                    "text": "I haven't touched lists in weeks—need a gentle re-entry.",
                    "sentiment": -0.05,
                    "days_ago": 14,
                }
            ],
            "olm_events": [
                {"action": "goal_set", "skill_id": "py101-data-structures", "target": 0.75, "days_ago": 20}
            ],
            "sentiment_topics": [],
            "baseline": {
                "results": {"py101-data-structures": "focus"},
                "scores": {"py101-data-structures": 0.48},
                "mastery_init": {"py101-data-structures": 0.35},
                "srl_profile": {"planning": 0.58, "monitoring": 0.5, "reflection": 0.44},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0073", "score": 0.76},
                    {"item_id": "py101_0077", "score": 0.72},
                    {"item_id": "py101_0081", "score": 0.68},
                ],
                "days_ago": 0,
            },
        },
        # ============================================================
        # P5: GOAL ATTAINMENT ACCELERATOR (ACCELERATING mode)
        # Entry: Active goals, progress rate ≥ 0.05/day
        # ============================================================
        {
            "scenario": "P5 — Goal attainment accelerator",
            "email": "dave@example.com",
            "arm": "T",
            "pref": "short",
            "mastery": [
                # All mastery values < 0.85 to avoid triggering CONSOLIDATING
                # (which is checked before ACCELERATING in mode priority)
                ("py101-foundations", 0.82),
                ("py101-control-flow", 0.78),
                ("py101-data-structures", 0.72),
                ("py101-functions", 0.65),  # Rapidly improving toward goal
            ],
            "goals": [("py101-functions", 0.85)],  # Active goal
            "impressions": [
                {
                    "item_id": "py101_0129",
                    "strategy": "hybrid",
                    "explain_level": "short",
                    "score": 0.85,
                    "source": "recs",
                    "days_ago": 2,
                }
            ],
            "clicks": [
                # Recent completions show high progress rate
                {
                    "item_id": "py101_0121",
                    "action": "complete",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "T",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 6,
                },
                {
                    "item_id": "py101_0125",
                    "action": "complete",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "T",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 4,
                },
                {
                    "item_id": "py101_0129",
                    "action": "complete",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "T",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 2,
                },
            ],
            "completions": [
                {"item_id": "py101_0121", "source": "player", "rank": 1, "strategy": "hybrid", "arm": "T", "course_id": PY101_COURSE_ID, "days_ago": 6},
                {"item_id": "py101_0125", "source": "player", "rank": 1, "strategy": "hybrid", "arm": "T", "course_id": PY101_COURSE_ID, "days_ago": 4},
                {"item_id": "py101_0129", "source": "player", "rank": 1, "strategy": "hybrid", "arm": "T", "course_id": PY101_COURSE_ID, "days_ago": 2},
            ],
            "explanations": [
                {
                    "item_id": "py101_0129",
                    "action": "expand",
                    "source": "recs",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "T",
                    "course_id": PY101_COURSE_ID,
                    "level": "detailed",
                    "dwell_ms": 520,
                    "days_ago": 2,
                }
            ],
            "feedback": [
                {
                    "item_id": "py101_0129",
                    "text": "Functions are clicking now! Making great progress.",
                    "rating": 5,
                    "polarity": 0.75,
                    "confidence": 0.85,
                    "days_ago": 2,
                }
            ],
            "reflections": [],
            "olm_events": [
                {"action": "goal_set", "skill_id": "py101-functions", "target": 0.85, "days_ago": 7}
            ],
            "sentiment_topics": [
                {
                    "topic": "functions_progress",
                    "mean": 0.65,
                    "slope": 0.12,
                    "intercept": 0.35,
                    "samples": 5,
                    "days_ago": 2,
                }
            ],
            "baseline": {
                "results": {"py101-functions": "advance"},
                "scores": {"py101-functions": 0.7},
                "mastery_init": {"py101-functions": 0.45},
                "srl_profile": {"planning": 0.72, "monitoring": 0.68, "reflection": 0.62},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0133", "score": 0.88},
                    {"item_id": "py101_0137", "score": 0.84},
                    {"item_id": "py101_0141", "score": 0.80},
                ],
                "days_ago": 0,
            },
        },
        # ============================================================
        # P6: MASTERY CONSOLIDATION (CONSOLIDATING mode)
        # Entry: Highest mastery ≥ 0.85, recent completions
        # ============================================================
        {
            "scenario": "P6 — Mastery consolidation",
            "email": "eve@example.com",
            "arm": "B",
            "pref": "auto",
            "mastery": [
                ("py101-foundations", 0.99),
                ("py101-control-flow", 0.98),
                ("py101-data-structures", 0.97),
                ("py101-functions", 0.96),
                ("py101-error-handling", 0.95),
                ("py101-file-ops", 0.94),
                ("py101-building-apps", 0.93),
            ],
            "goals": [],
            "impressions": [
                {
                    "item_id": "py101_0153",
                    "strategy": "hybrid",
                    "explain_level": "auto",
                    "score": 0.84,
                    "source": "recs",
                    "days_ago": 1,
                }
            ],
            "clicks": [
                {
                    "item_id": "py101_0153",
                    "action": "complete",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "B",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 2,  # Recent completion
                }
            ],
            # All 192 items completed — makes Eve eligible for the certificate
            "completions": [
                {
                    "item_id": f"py101_{i:04d}",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "B",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": max(0, 192 - i),  # Spread over time
                }
                for i in range(1, 193)
            ],
            "explanations": [],
            "feedback": [],
            "reflections": [],
            "olm_events": [],
            "sentiment_topics": [],
            "baseline": {
                "results": {"py101-error-handling": "maintain"},
                "scores": {"py101-error-handling": 0.85},
                "mastery_init": {"py101-error-handling": 0.78},
                "srl_profile": {"planning": 0.78, "monitoring": 0.75, "reflection": 0.72},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0157", "score": 0.86},
                    {"item_id": "py101_0161", "score": 0.82},
                    {"item_id": "py101_0165", "score": 0.78},
                ],
                "days_ago": 0,
            },
        },
        # ============================================================
        # P7: DEFAULT HYBRID PATHWAY (NOMINAL mode)
        # Entry: Normal engagement, balanced mastery
        # This is the steady-state fallback for most learners
        # ============================================================
        {
            "scenario": "P7 — Default hybrid pathway (nominal)",
            "email": "notag@example.com",
            "arm": "A",
            "pref": "short",
            "mastery": [
                ("py101-foundations", 0.78),
                ("py101-control-flow", 0.65),
                ("py101-data-structures", 0.52),  # Balanced, no extremes
            ],
            "goals": [],
            "impressions": [
                {
                    "item_id": "py101_0081",
                    "strategy": "hybrid",
                    "explain_level": "short",
                    "score": 0.72,
                    "source": "recs",
                    "days_ago": 1,
                }
            ],
            "clicks": [
                {
                    "item_id": "py101_0081",
                    "action": "click",
                    "source": "recs",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "A",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 1,
                }
            ],
            "completions": [
                {
                    "item_id": "py101_0077",
                    "source": "player",
                    "rank": 1,
                    "strategy": "hybrid",
                    "arm": "A",
                    "course_id": PY101_COURSE_ID,
                    "days_ago": 3,
                }
            ],
            "explanations": [],
            "feedback": [],
            "reflections": [],
            "olm_events": [],
            "sentiment_topics": [],
            "baseline": {
                "results": {"py101-data-structures": "continue"},
                "scores": {"py101-data-structures": 0.55},
                "mastery_init": {"py101-data-structures": 0.45},
                "srl_profile": {"planning": 0.55, "monitoring": 0.52, "reflection": 0.48},
            },
            "arl_decision": {
                "policy_name": "hybrid",
                "strategy": "hybrid",
                "items": [
                    {"item_id": "py101_0085", "score": 0.74},
                    {"item_id": "py101_0089", "score": 0.70},
                    {"item_id": "py101_0093", "score": 0.66},
                ],
                "days_ago": 0,
            },
        },
    ]

    # ------------------------------------------------------------
    # Create all learner records with telemetry
    # ------------------------------------------------------------
    for u in learners:
        lid = str(uuid.uuid5(uuid.NAMESPACE_DNS, u["email"]))

        user = User(email=u["email"], learner_id=lid)
        db.add(user)
        db.flush()
        user_id = user.id

        db.add(GroupAssignment(learner_id=lid, arm=u["arm"]))
        db.add(LearnerConsent(learner_id=lid, consent_given=True))
        db.add(LearnerPreference(learner_id=lid, explain_level=u["pref"]))

        mastery_records = []
        for sid, val in u["mastery"]:
            m = Mastery(learner_id=lid, skill_id=sid, value=val)
            db.add(m)
            mastery_records.append((sid, val, m))
        db.flush()
        for sid, val, mastery_row in mastery_records:
            evidence_item = f"py101_0001"
            evidence = MasteryEvidence(
                learner_id=lid,
                skill_id=sid,
                source="seed_demo.assessment",
                delta=val,
                resulting_value=val,
                item_id=evidence_item,
                notes="Initial mastery estimate from seeding script",
                metadata_json=json.dumps({"origin": "seed_demo"}, sort_keys=True),
            )
            db.add(evidence)
            mastery_row.last_evidence = evidence

        for sid, target in u.get("goals", []):
            db.add(
                Goal(
                    learner_id=lid,
                    skill_id=sid,
                    target=target,
                    due_date=now + dt.timedelta(days=28),
                )
            )

        for event in u.get("olm_events", []):
            created = ts_days_ago(event.get("days_ago", 0))
            db.add(
                OLMEvent(
                    learner_id=lid,
                    skill_id=event["skill_id"],
                    action=event["action"],
                    target=event.get("target"),
                    created_at=created,
                    updated_at=created,
                )
            )

        for idx, entry in enumerate(u.get("impressions", []), start=1):
            item_id = entry["item_id"]
            strategy = entry["strategy"]
            explain_level = entry.get("explain_level")
            score = entry.get("score")
            source = entry.get("source", "recs")
            created = ts_days_ago(entry.get("days_ago", 0))
            db.add(
                Impression(
                    user_id=user_id,
                    learner_id=lid,
                    item_id=item_id,
                    source=source,
                    rank=idx,
                    strategy=strategy,
                    arm=u["arm"],
                    arm_key=u["arm"],
                    policy_version=routine_version,
                    schema_version=schema_version,
                    explain_level=explain_level,
                    score=score,
                    course_id=PY101_COURSE_ID,
                    request_id=f"{lid}-{item_id}-imp{idx}",
                    created_at=created,
                    updated_at=created,
                )
            )

        for click in u.get("clicks", []):
            item_id = click["item_id"]
            action = click["action"]
            source = click.get("source", "recs")
            rank = click.get("rank")
            strategy = click.get("strategy")
            arm_value = click.get("arm", u["arm"])
            course_id = click.get("course_id", PY101_COURSE_ID)
            created = ts_days_ago(click.get("days_ago", 0))
            click_row = Click(
                user_id=user_id,
                learner_id=lid,
                item_id=item_id,
                action=action,
                source=source,
                rank=rank,
                strategy=strategy,
                arm=arm_value,
                arm_key=arm_value,
                policy_version=routine_version,
                schema_version=schema_version,
                course_id=course_id,
                created_at=created,
                updated_at=created,
            )
            db.add(click_row)
            if action == "complete":
                db.add(
                    Completion(
                        user_id=user_id,
                        learner_id=lid,
                        item_id=item_id,
                        source=source,
                        rank=rank,
                        strategy=strategy,
                        arm=arm_value,
                        arm_key=arm_value,
                        policy_version=routine_version,
                        schema_version=schema_version,
                        course_id=course_id,
                        request_id=f"{lid}-{item_id}-complete",
                        created_at=created,
                        updated_at=created,
                    )
                )

        for comp in u.get("completions", []):
            # Check if already added via clicks
            item_id = comp["item_id"]
            source = comp.get("source", "player")
            rank = comp.get("rank")
            strategy = comp.get("strategy")
            arm_value = comp.get("arm", u["arm"])
            course_id = comp.get("course_id", PY101_COURSE_ID)
            created = ts_days_ago(comp.get("days_ago", 0))
            # Only add if not already added via click action
            existing = [c for c in u.get("clicks", []) if c.get("item_id") == item_id and c.get("action") == "complete"]
            if not existing:
                db.add(
                    Completion(
                        user_id=user_id,
                        learner_id=lid,
                        item_id=item_id,
                        source=source,
                        rank=rank,
                        strategy=strategy,
                        arm=arm_value,
                        arm_key=arm_value,
                        policy_version=routine_version,
                        schema_version=schema_version,
                        course_id=course_id,
                        request_id=f"{lid}-{item_id}-complete",
                        created_at=created,
                        updated_at=created,
                    )
                )

        for exp in u.get("explanations", []):
            item_id = exp["item_id"]
            action = exp.get("action", "expand")
            source = exp.get("source", "recs")
            rank = exp.get("rank")
            strategy = exp.get("strategy")
            arm_value = exp.get("arm", u["arm"])
            course_id = exp.get("course_id", PY101_COURSE_ID)
            level = exp.get("level")
            dwell = exp.get("dwell_ms")
            created = ts_days_ago(exp.get("days_ago", 0))
            db.add(
                ExplanationInteraction(
                    user_id=user_id,
                    learner_id=lid,
                    item_id=item_id,
                    action=action,
                    source=source,
                    rank=rank,
                    strategy=strategy,
                    arm=arm_value,
                    arm_key=arm_value,
                    policy_version=routine_version,
                    schema_version=schema_version,
                    course_id=course_id,
                    level=level,
                    dwell_ms=dwell,
                    created_at=created,
                    updated_at=created,
                )
            )

        for fb in u.get("feedback", []):
            item_id = fb["item_id"]
            text = fb["text"]
            rating = fb.get("rating")
            polarity = fb.get("polarity", 0.0)
            confidence = fb.get("confidence", 0.0)
            created = ts_days_ago(fb.get("days_ago", 0))
            db.add(
                Feedback(
                    learner_id=lid,
                    item_id=item_id,
                    text=text,
                    rating=rating,
                    created_at=created,
                    updated_at=created,
                )
            )
            db.add(
                SentimentScore(
                    learner_id=lid,
                    item_id=item_id,
                    polarity=polarity,
                    confidence=confidence,
                    created_at=created,
                    updated_at=created,
                )
            )
            db.add(
                ItemSentimentAgg(
                    item_id=item_id,
                    mean_polarity=polarity,
                    n=1,
                    stdev=0.0,
                    created_at=created,
                    updated_at=created,
                )
            )
            db.add(
                LearnerSentimentWindow(
                    learner_id=lid,
                    mean_polarity_7d=polarity,
                    n_7d=1,
                    created_at=created,
                    updated_at=created,
                )
            )

        for topic_entry in u.get("sentiment_topics", []):
            created = ts_days_ago(topic_entry.get("days_ago", 0))
            db.add(
                SentimentAggregate(
                    learner_id=lid,
                    topic=topic_entry["topic"],
                    mean_polarity=topic_entry["mean"],
                    slope=topic_entry["slope"],
                    intercept=topic_entry["intercept"],
                    sample_size=topic_entry.get("samples", 1),
                    window_days=7,
                    last_sample_at=created,
                )
            )

        for reflection in u.get("reflections", []):
            created = ts_days_ago(reflection.get("days_ago", 0))
            db.add(
                Reflection(
                    user_id=user_id,
                    learner_id=lid,
                    item_id=reflection.get("item_id"),
                    topic=reflection.get("topic"),
                    prompt="self_reflection",
                    text=reflection["text"],
                    sentiment=reflection.get("sentiment"),
                    arm_key=u["arm"],
                    policy_version=routine_version,
                    schema_version=schema_version,
                    created_at=created,
                    updated_at=created,
                )
            )

        decision_meta = u.get("arl_decision")
        if decision_meta and decision_meta.get("items"):
            decision_id = f"{lid}-decision"
            decision_created = ts_days_ago(decision_meta.get("days_ago", 0))
            request_payload = {
                "learner_id": lid,
                "requested_at": decision_created.isoformat(),
                "top_k": len(decision_meta["items"]),
                "strategy": decision_meta.get("strategy"),
            }
            response_payload = {
                "items": decision_meta["items"],
                "policy_name": decision_meta["policy_name"],
                "routine_version": routine_version,
                "arm": u["arm"],
            }
            decision = ARLDecision(
                decision_id=decision_id,
                learner_id=lid,
                policy_name=decision_meta["policy_name"],
                policy_version=routine_version,
                deterministic_hash=f"{lid[:12]}-{decision_meta['policy_name']}",
                seed=str(100 + len(decision_meta["items"])),
                request_id=f"{lid}-arl-req",
                request_payload=json.dumps(request_payload, sort_keys=True),
                response_payload=json.dumps(response_payload, sort_keys=True),
                created_at=decision_created,
                updated_at=decision_created,
            )
            db.add(decision)
            for idx, item in enumerate(decision_meta["items"], start=1):
                db.add(
                    ARLOutcome(
                        decision_id=decision_id,
                        item_id=item.get("item_id"),
                        rank=idx,
                        score=item.get("score"),
                        features_json=json.dumps(
                            {"target_skill": item.get("item_id", "unknown")},
                            sort_keys=True,
                        ),
                        weights_json=json.dumps(
                            {"weight": item.get("score", 0.0)}, sort_keys=True
                        ),
                        metadata_json=json.dumps(
                            {"arm": u["arm"], "strategy": decision_meta.get("strategy")},
                            sort_keys=True,
                        ),
                        created_at=decision_created,
                        updated_at=decision_created,
                    )
                )

    db.commit()
    db.close()

    print("Seeded PY101 course:")
    print("  - PY101: Python Fundamentals for Beginners (Skulpt)")
    print(f"  - {len(items)} learning items across 7 modules")
    print(f"  - {len(learners)} demo learners demonstrating all controller modes")
    print("\nThree-group design:")
    print("  T = Treatment (governed adaptive + structured explanations)")
    print("  A = Control A (model-driven adaptive + basic explanations)")
    print("  B = Control B (progress display, no structured explanations)")
    print("\nDemo Learners by Control Routine:")
    for learner in learners:
        scenario = learner["scenario"]
        email = learner["email"]
        arm = learner["arm"]
        print(f"  - {email} (Group {arm}): {scenario}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed X-ELRA demo data")
    parser.add_argument(
        "--no-reset",
        action="store_true",
        default=os.environ.get("SEED_NO_RESET", "").lower() in ("1", "true", "yes"),
        help="Skip dropping/recreating tables (keep existing data). Also settable via SEED_NO_RESET=1 env var.",
    )
    parser.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Skip interactive confirmation prompt.",
    )
    args = parser.parse_args()
    do_reset = not args.no_reset
    if do_reset and not args.yes:
        db_url = str(engine.url)
        answer = input(
            f"This will DROP ALL TABLES in {db_url}. Continue? [y/N] "
        )
        if answer.strip().lower() not in ("y", "yes"):
            print("Aborted.")
            raise SystemExit(1)
    seed(reset=do_reset)
