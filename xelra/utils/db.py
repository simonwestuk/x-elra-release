"""Database engine/session setup plus SQLAlchemy models and persistence helpers."""

from __future__ import annotations

import hashlib
import datetime as dt
import json
from typing import Dict, Optional

from sqlalchemy import (
    create_engine,
    text as sa_text,
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    Text,
    ForeignKey,
    Index,
    UniqueConstraint,
    event,
    inspect,
)
from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
    relationship,
    declared_attr,
)

from ..config import settings


def _is_sqlite(uri: str) -> bool:
    """Check if the database URI is for SQLite."""
    return uri.startswith("sqlite:")


def _ensure_pg_database_exists(uri: str) -> None:
    """Create the PostgreSQL database if it does not already exist.

    Connects to the default 'postgres' maintenance database, checks whether the
    target database exists, and issues CREATE DATABASE if needed.  This is a
    no-op for SQLite URIs.
    """
    if _is_sqlite(uri):
        return

    from sqlalchemy.engine.url import make_url

    url = make_url(uri)
    target_db = url.database
    if not target_db:
        return

    # Build a URL that points at the default 'postgres' database
    maintenance_url = url.set(database="postgres")

    try:
        tmp_engine = create_engine(maintenance_url, isolation_level="AUTOCOMMIT")
        with tmp_engine.connect() as conn:
            result = conn.execute(
                # Use text() for raw SQL
                sa_text(
                    "SELECT 1 FROM pg_database WHERE datname = :dbname"
                ),
                {"dbname": target_db},
            )
            if not result.scalar():
                # Database does not exist – create it
                # CREATE DATABASE cannot be parameterised, but target_db comes
                # from our own connection URI, not user input.
                conn.execute(
                    sa_text(
                        f'CREATE DATABASE "{target_db}"'
                    )
                )
                print(f"[db] Created PostgreSQL database '{target_db}'")
            else:
                print(f"[db] PostgreSQL database '{target_db}' already exists")
        tmp_engine.dispose()
    except Exception as exc:
        # Log but don't crash – the main engine creation will produce a
        # clearer error if the database truly cannot be reached.
        print(f"[db] Could not auto-create database '{target_db}': {exc}")


def _create_engine_with_options(uri: str):
    """Create SQLAlchemy engine with appropriate options for the database type."""
    if _is_sqlite(uri):
        # SQLite-specific settings
        return create_engine(uri, echo=False, future=True)
    else:
        # Ensure the PostgreSQL database exists before connecting
        _ensure_pg_database_exists(uri)
        # PostgreSQL and other databases - add pool settings for production
        return create_engine(
            uri,
            echo=False,
            future=True,
            pool_pre_ping=True,  # Verify connections before use
            pool_size=5,
            max_overflow=10,
        )


engine = _create_engine_with_options(settings.database_uri)


# Ensure SQLite enforces foreign keys (only applies to SQLite)
@event.listens_for(engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    # Only run PRAGMA for SQLite connections
    if not _is_sqlite(settings.database_uri):
        return
    try:
        cur = dbapi_connection.cursor()
        cur.execute("PRAGMA foreign_keys=ON")
        cur.close()
    except Exception:
        # Safe to ignore if not SQLite
        pass


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)


class TimestampMixin:
    """Mixin ensuring created/updated timestamps on all write models."""

    @declared_attr
    def created_at(cls):  # type: ignore[override]
        return Column(DateTime, default=utc_now, nullable=False)

    @declared_attr
    def updated_at(cls):  # type: ignore[override]
        return Column(
            DateTime,
            default=utc_now,
            onupdate=utc_now,
            nullable=False,
        )


class RoutineVersionPropertyMixin:
    """Provide ``routine_version`` alias for legacy ``policy_version`` columns."""

    @property
    def routine_version(self) -> Optional[str]:  # type: ignore[override]
        return getattr(self, "policy_version", None)

    @routine_version.setter
    def routine_version(self, value: Optional[str]) -> None:  # type: ignore[override]
        setattr(self, "policy_version", value)


# -------------------------
# Core user/auth entities
# -------------------------


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, unique=True, nullable=False)
    learner_id = Column(String, index=True, unique=True, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # ORM relationships
    consents = relationship(
        "LearnerConsent", back_populates="user", passive_deletes=True
    )
    group_assignment = relationship(
        "GroupAssignment", back_populates="user", uselist=False, passive_deletes=True
    )
    preferences = relationship(
        "LearnerPreference", back_populates="user", uselist=False, passive_deletes=True
    )
    masteries = relationship("Mastery", back_populates="user", passive_deletes=True)
    goals = relationship("Goal", back_populates="user", passive_deletes=True)
    impressions = relationship("Impression", passive_deletes=True)
    clicks = relationship("Click", passive_deletes=True)
    explanation_interactions = relationship(
        "ExplanationInteraction", passive_deletes=True
    )
    feedback = relationship("Feedback", back_populates="user", passive_deletes=True)
    completions = relationship("Completion", passive_deletes=True)
    reflections = relationship("Reflection", passive_deletes=True)
    sentiment_scores = relationship("SentimentScore", passive_deletes=True)
    sentiment_aggregates = relationship("SentimentAggregate", passive_deletes=True)
    sentiment_window = relationship(
        "LearnerSentimentWindow",
        back_populates="user",
        uselist=False,
        passive_deletes=True,
    )
    olm_events = relationship("OLMEvent", back_populates="user", passive_deletes=True)
    live_code_events = relationship(
        "LiveCodeEvent", back_populates="user", passive_deletes=True
    )
    mastery_evidence = relationship(
        "MasteryEvidence", back_populates="user", passive_deletes=True
    )
    arl_decisions = relationship(
        "ARLDecision", back_populates="user", passive_deletes=True
    )


class LoginCode(TimestampMixin, Base):
    __tablename__ = "login_codes"

    id = Column(Integer, primary_key=True)
    email = Column(String, index=True, nullable=False)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)


# -------------------------
# Study and assignment
# -------------------------


class LearnerConsent(TimestampMixin, Base):
    __tablename__ = "learner_consent"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    consent_given = Column(Boolean, default=False, nullable=False)
    timestamp = Column(DateTime, default=utc_now, nullable=False)

    user = relationship("User", back_populates="consents", passive_deletes=True)


class GroupAssignment(TimestampMixin, Base):
    __tablename__ = "group_assignment"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        unique=True,
        nullable=False,
    )
    arm = Column(String, nullable=False)  # 'T' (Treatment), 'A' (Control A), 'B' (Control B)
    assigned_at = Column(DateTime, default=utc_now, nullable=False)
    seed = Column(String, nullable=True)

    user = relationship("User", back_populates="group_assignment", passive_deletes=True)


# -------------------------
# Catalogue and skills
# -------------------------


class Item(TimestampMixin, Base):
    __tablename__ = "items"

    item_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    topics = Column(String, nullable=True)
    popularity = Column(Float, default=0.5, nullable=False)
    url = Column(String, nullable=True)
    course_id = Column(String, nullable=True)
    type = Column(String, nullable=True)
    duration_mins = Column(Integer, default=0, nullable=True)
    prereqs = Column(String, nullable=True)

    # ORM relationships
    item_skills = relationship(
        "ItemSkill",
        back_populates="item",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    impressions = relationship("Impression", passive_deletes=True)
    clicks = relationship("Click", passive_deletes=True)
    explanation_interactions = relationship(
        "ExplanationInteraction", passive_deletes=True
    )
    feedback = relationship("Feedback", back_populates="item", passive_deletes=True)
    sentiment_scores = relationship(
        "SentimentScore", back_populates="item", passive_deletes=True
    )
    sentiment_agg = relationship(
        "ItemSentimentAgg", back_populates="item", uselist=False, passive_deletes=True
    )
    completions = relationship("Completion", passive_deletes=True)
    reflections = relationship("Reflection", passive_deletes=True)
    mastery_evidence = relationship(
        "MasteryEvidence", back_populates="item", passive_deletes=True
    )
    live_code_events = relationship(
        "LiveCodeEvent", back_populates="item", passive_deletes=True
    )


class Skill(TimestampMixin, Base):
    __tablename__ = "skills"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    # difficulty level for sequencing (1..5)
    level = Column(Integer, nullable=True)

    # ORM relationships
    item_skills = relationship(
        "ItemSkill",
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    masteries = relationship(
        "Mastery",
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    goals = relationship(
        "Goal",
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    # New: OLM telemetry events
    olm_events = relationship("OLMEvent", back_populates="skill", passive_deletes=True)
    mastery_evidence = relationship(
        "MasteryEvidence", back_populates="skill", passive_deletes=True
    )

    prerequisites = relationship(
        "SkillPrerequisite",
        back_populates="skill",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="SkillPrerequisite.skill_id",
    )
    dependents = relationship(
        "SkillPrerequisite",
        back_populates="prerequisite",
        cascade="all, delete-orphan",
        passive_deletes=True,
        foreign_keys="SkillPrerequisite.prerequisite_skill_id",
    )


class ItemSkill(TimestampMixin, Base):
    __tablename__ = "item_skills"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(
        String, ForeignKey("items.item_id", ondelete="CASCADE"), nullable=False
    )
    skill_id = Column(
        String, ForeignKey("skills.id", ondelete="CASCADE"), nullable=False
    )
    weight = Column(Float, nullable=True)  # contribution weight (0..1)

    # ORM relationships
    item = relationship("Item", back_populates="item_skills", passive_deletes=True)
    skill = relationship("Skill", back_populates="item_skills", passive_deletes=True)

    __table_args__ = (
        Index("ix_item_skills_item_skill", "item_id", "skill_id", unique=True),
    )


class SkillPrerequisite(TimestampMixin, Base):
    __tablename__ = "skill_prerequisites"

    id = Column(Integer, primary_key=True, autoincrement=True)
    skill_id = Column(
        String,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    prerequisite_skill_id = Column(
        String,
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill = relationship(
        "Skill",
        foreign_keys=[skill_id],
        back_populates="prerequisites",
        passive_deletes=True,
    )
    prerequisite = relationship(
        "Skill",
        foreign_keys=[prerequisite_skill_id],
        back_populates="dependents",
        passive_deletes=True,
    )

    __table_args__ = (
        Index(
            "ix_skill_prerequisites_skill_prerequisite",
            "skill_id",
            "prerequisite_skill_id",
            unique=True,
        ),
        UniqueConstraint("skill_id", "prerequisite_skill_id"),
    )


# -------------------------
# Preferences and tracking
# -------------------------


class LearnerPreference(TimestampMixin, Base):
    __tablename__ = "learner_preferences"

    learner_id = Column(
        String, ForeignKey("users.learner_id", ondelete="CASCADE"), primary_key=True
    )
    explain_level = Column(String, nullable=False, default="auto")

    user = relationship("User", back_populates="preferences", passive_deletes=True)


class Impression(RoutineVersionPropertyMixin, TimestampMixin, Base):
    __tablename__ = "impressions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    source = Column(String, nullable=True)  # e.g., 'next_up', 'recs'
    rank = Column(Integer, nullable=True)
    strategy = Column(String, nullable=False)
    arm = Column(String, nullable=False)
    arm_key = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    schema_version = Column(String, nullable=True)
    explain_level = Column(String, nullable=True)
    score = Column(Float, nullable=True)
    course_id = Column(String, nullable=True)
    request_id = Column(String, index=True, nullable=True)
    # TimestampMixin supplies created_at/updated_at

    


class Click(RoutineVersionPropertyMixin, TimestampMixin, Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    action = Column(String, nullable=False)  # e.g., 'click' | 'complete'
    source = Column(String, nullable=True)  # e.g., 'next_up', 'recs'
    rank = Column(Integer, nullable=True)
    strategy = Column(String, nullable=True)
    arm = Column(String, nullable=True)
    arm_key = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    schema_version = Column(String, nullable=True)
    course_id = Column(String, nullable=True)
    # TimestampMixin supplies created_at/updated_at

    


class Completion(RoutineVersionPropertyMixin, TimestampMixin, Base):
    __tablename__ = "completions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    source = Column(String, nullable=True)
    rank = Column(Integer, nullable=True)
    strategy = Column(String, nullable=True)
    arm = Column(String, nullable=True)
    arm_key = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    schema_version = Column(String, nullable=True)
    course_id = Column(String, nullable=True)
    request_id = Column(String, nullable=True, index=True)

    


Index(
    "ix_completions_learner_item",
    Completion.learner_id,
    Completion.item_id,
    Completion.created_at,
)


# -------------------------
# Recommendation decisions
# -------------------------


class ARLDecision(RoutineVersionPropertyMixin, TimestampMixin, Base):
    __tablename__ = "arl_decisions"

    id = Column(Integer, primary_key=True)
    decision_id = Column(String(64), unique=True, index=True, nullable=False)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    policy_name = Column("routine_name", String, nullable=False)
    policy_version = Column("routine_version", String(64), nullable=False)
    deterministic_hash = Column(String(128), index=True, nullable=False)
    seed = Column(String(64), nullable=True)
    request_id = Column(String, index=True, nullable=True)
    request_payload = Column(Text, nullable=False)
    response_payload = Column(Text, nullable=False)

    @property
    def routine_name(self) -> str:
        return self.policy_name

    @routine_name.setter
    def routine_name(self, value: str) -> None:
        self.policy_name = value

    user = relationship("User", back_populates="arl_decisions", passive_deletes=True)
    outcomes = relationship(
        "ARLOutcome",
        back_populates="decision",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    feature_snapshots = relationship(
        "FeatureSnapshot",
        back_populates="decision",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ARLOutcome(TimestampMixin, Base):
    __tablename__ = "arl_outcomes"

    id = Column(Integer, primary_key=True)
    decision_id = Column(
        String(64),
        ForeignKey("arl_decisions.decision_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(String, index=True, nullable=True)
    rank = Column(Integer, nullable=False)
    score = Column(Float, nullable=True)
    features_json = Column(Text, nullable=True)
    weights_json = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)

    decision = relationship("ARLDecision", back_populates="outcomes")


Index(
    "ix_arl_outcomes_decision_rank",
    ARLOutcome.decision_id,
    ARLOutcome.rank,
    unique=True,
)


class FeatureSnapshot(TimestampMixin, Base):
    __tablename__ = "feature_snapshots"

    id = Column(Integer, primary_key=True)
    decision_id = Column(
        String(64),
        ForeignKey("arl_decisions.decision_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(String, nullable=False)
    rank = Column(Integer, nullable=False)
    features_json = Column(Text, nullable=True)
    weights_json = Column(Text, nullable=True)

    decision = relationship("ARLDecision", back_populates="feature_snapshots")


Index(
    "ix_feature_snapshots_decision_rank",
    FeatureSnapshot.decision_id,
    FeatureSnapshot.rank,
    unique=True,
)


class ExplanationInteraction(RoutineVersionPropertyMixin, TimestampMixin, Base):
    __tablename__ = "explanation_interactions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True, nullable=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    action = Column(String, nullable=False)  # e.g., 'expand','collapse','view'
    source = Column(String, nullable=True)  # e.g., 'next_up', 'recs'
    rank = Column(Integer, nullable=True)
    strategy = Column(String, nullable=True)
    arm = Column(String, nullable=True)
    arm_key = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    schema_version = Column(String, nullable=True)
    course_id = Column(String, nullable=True)
    level = Column(String, nullable=True)  # 'short','detailed'
    dwell_ms = Column(Integer, nullable=True)
    # TimestampMixin supplies created_at/updated_at

    


# -------------------------
# Mastery, goals, feedback
# -------------------------


class MasteryEvidence(TimestampMixin, Base):
    __tablename__ = "mastery_evidence"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id = Column(
        String, ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    source = Column(String, nullable=False)
    delta = Column(Float, nullable=True)
    resulting_value = Column(Float, nullable=True)
    item_id = Column(
        String, ForeignKey("items.item_id", ondelete="SET NULL"), index=True, nullable=True
    )
    notes = Column(Text, nullable=True)
    metadata_json = Column(Text, nullable=True)

    user = relationship("User", back_populates="mastery_evidence", passive_deletes=True)
    skill = relationship("Skill", back_populates="mastery_evidence", passive_deletes=True)
    item = relationship("Item", back_populates="mastery_evidence", passive_deletes=True)
    masteries = relationship(
        "Mastery", back_populates="last_evidence", passive_deletes=True
    )


class Mastery(TimestampMixin, Base):
    __tablename__ = "mastery"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id = Column(
        String, ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    value = Column(Float, nullable=False, default=0.0)  # 0..1
    p = Column(Float, nullable=False, default=0.0)
    sigma = Column(Float, nullable=False, default=1.0)
    last_evidence_id = Column(
        Integer,
        ForeignKey("mastery_evidence.id", ondelete="SET NULL"),
        nullable=True,
    )

    # ORM relationships
    skill = relationship("Skill", back_populates="masteries", passive_deletes=True)
    user = relationship("User", back_populates="masteries", passive_deletes=True)
    last_evidence = relationship(
        "MasteryEvidence", back_populates="masteries", passive_deletes=True
    )

    __table_args__ = (
        Index("ix_mastery_learner_skill", "learner_id", "skill_id", unique=True),
    )


class Goal(TimestampMixin, Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id = Column(
        String, ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    target = Column(Float, nullable=False, default=1.0)  # 0..1
    due_date = Column(DateTime, nullable=True)

    # ORM relationships
    skill = relationship("Skill", back_populates="goals", passive_deletes=True)
    user = relationship("User", back_populates="goals", passive_deletes=True)


class Feedback(TimestampMixin, Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)

    user = relationship("User", back_populates="feedback", passive_deletes=True)
    item = relationship("Item", back_populates="feedback", passive_deletes=True)


class Reflection(RoutineVersionPropertyMixin, TimestampMixin, Base):
    __tablename__ = "reflections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    topic = Column(String, nullable=True)
    prompt = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    sentiment = Column(Float, nullable=True)
    metadata_json = Column(Text, nullable=True)
    arm_key = Column(String, nullable=True)
    policy_version = Column(String, nullable=True)
    schema_version = Column(String, nullable=True)

    


Index(
    "ix_reflections_learner_topic",
    Reflection.learner_id,
    Reflection.topic,
)


# New: OLM telemetry events (goal_set, goal_clear)
class OLMEvent(TimestampMixin, Base):
    __tablename__ = "olm_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    skill_id = Column(
        String, ForeignKey("skills.id", ondelete="CASCADE"), index=True, nullable=False
    )
    action = Column(String, nullable=False)  # 'goal_set' | 'goal_clear'
    target = Column(Float, nullable=True)  # optional target when setting/updating

    user = relationship("User", back_populates="olm_events", passive_deletes=True)
    skill = relationship("Skill", back_populates="olm_events", passive_deletes=True)


class LiveCodeEvent(TimestampMixin, Base):
    __tablename__ = "live_code_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, index=True, nullable=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    attempt_id = Column(String, nullable=True)
    session_id = Column(String, nullable=True)
    event = Column(String, index=True, nullable=False)
    cell_id = Column(String, nullable=True)
    engine = Column(String, nullable=True)
    status = Column(String, nullable=True)
    code_size = Column(Integer, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    output_preview = Column(Text, nullable=True)
    error_type = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    response_text = Column(Text, nullable=True)
    message_text = Column(Text, nullable=True)
    event_at = Column(DateTime, index=True, nullable=False, default=utc_now)
    extra_json = Column(Text, nullable=True)

    user = relationship("User", back_populates="live_code_events", passive_deletes=True)
    item = relationship("Item", back_populates="live_code_events", passive_deletes=True)


# -------------------------
# Sentiment analytics
# -------------------------


class SentimentScore(TimestampMixin, Base):
    __tablename__ = "sentiment_scores"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    item_id = Column(
        String,
        ForeignKey("items.item_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    polarity = Column(Float, nullable=False)  # -1..1
    confidence = Column(Float, nullable=False)  # 0..1

    item = relationship("Item", back_populates="sentiment_scores", passive_deletes=True)


class SentimentAggregate(TimestampMixin, Base):
    __tablename__ = "sentiment_aggregate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    topic = Column(String, nullable=False)
    mean_polarity = Column(Float, default=0.0, nullable=False)
    slope = Column(Float, default=0.0, nullable=False)
    intercept = Column(Float, default=0.0, nullable=False)
    sample_size = Column(Integer, default=0, nullable=False)
    window_days = Column(Integer, default=7, nullable=False)
    last_sample_at = Column(DateTime, nullable=True)



Index(
    "ix_sentiment_aggregate_learner_topic",
    SentimentAggregate.learner_id,
    SentimentAggregate.topic,
    unique=True,
)


class ItemSentimentAgg(TimestampMixin, Base):
    __tablename__ = "item_sentiment_agg"

    item_id = Column(
        String, ForeignKey("items.item_id", ondelete="CASCADE"), primary_key=True
    )
    mean_polarity = Column(Float, default=0.0, nullable=False)
    n = Column(Integer, default=0, nullable=False)
    stdev = Column(Float, default=0.0, nullable=False)

    item = relationship("Item", back_populates="sentiment_agg", passive_deletes=True)


class LearnerSentimentWindow(TimestampMixin, Base):
    __tablename__ = "learner_sentiment_window"

    learner_id = Column(
        String, ForeignKey("users.learner_id", ondelete="CASCADE"), primary_key=True
    )
    mean_polarity_7d = Column(Float, default=0.0, nullable=False)
    n_7d = Column(Integer, default=0, nullable=False)

    user = relationship("User", back_populates="sentiment_window", passive_deletes=True)


class SurveyCompletion(TimestampMixin, Base):
    """Track periodic survey completions for pilot study."""

    __tablename__ = "survey_completions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    survey_week = Column(Integer, nullable=False)  # 4, 8, or 12
    completed_at = Column(DateTime, default=utc_now, nullable=False)

    __table_args__ = (
        Index("ix_survey_completions_learner_week", "learner_id", "survey_week", unique=True),
    )


class Certificate(TimestampMixin, Base):
    """Participation certificate issued when a learner completes all course items."""

    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    course_id = Column(String, nullable=True)
    holder_name = Column(String, nullable=True)
    issued_at = Column(DateTime, default=utc_now, nullable=False)
    total_items = Column(Integer, nullable=False, default=0)
    total_completions = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        Index("ix_certificates_learner_course", "learner_id", "course_id", unique=True),
    )


class ReminderLog(TimestampMixin, Base):
    """Tracks engagement reminders sent to learners."""

    __tablename__ = "reminder_logs"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    reminder_type = Column(String, nullable=False)  # 'inactive_7d', 'inactive_14d'
    sent_at = Column(DateTime, default=utc_now, nullable=False)


class ReminderConfig(TimestampMixin, Base):
    """Admin-configurable settings for engagement reminder emails.

    Single-row table (id=1). Stores frequency, cooldown thresholds,
    and email template content so admins can adjust without code changes.
    """

    __tablename__ = "reminder_config"

    id = Column(Integer, primary_key=True)
    # How often (in hours) the background check runs
    check_interval_hours = Column(Integer, nullable=False, default=24)
    # Minimum days between reminders to the same learner
    cooldown_days = Column(Integer, nullable=False, default=7)
    # Risk-level thresholds (days inactive)
    warning_days = Column(Integer, nullable=False, default=7)
    critical_days = Column(Integer, nullable=False, default=14)
    # Email template
    email_subject = Column(String, nullable=False, default="We miss you on X-ELRA!")
    email_heading = Column(
        String,
        nullable=False,
        default="Keep your learning momentum going",
    )
    email_body = Column(
        Text,
        nullable=False,
        default=(
            "It's been {days_inactive} days since your last activity on X-ELRA. "
            "You've completed {total_completions} item(s) so far — great work!\n\n"
            "New recommendations are waiting for you. Pop in for just a few "
            "minutes to continue building your skills."
        ),
    )
    email_cta_text = Column(String, nullable=False, default="Continue Learning")
    # Whether automatic reminders are enabled at all
    enabled = Column(Boolean, nullable=False, default=True)


class SurveyConfig(TimestampMixin, Base):
    """Admin-configurable settings for pilot study surveys.

    Single-row table (id=1). Stores the current completion code
    that learners must enter to verify they completed the survey.
    """

    __tablename__ = "survey_config"

    id = Column(Integer, primary_key=True)
    # Current completion code (displayed at end of JISC survey)
    completion_code = Column(String, nullable=True, default=None)
    # Whether code verification is enabled
    code_required = Column(Boolean, nullable=False, default=False)


class ConsentConfig(TimestampMixin, Base):
    """Admin-configurable settings for consent form verification.

    Single-row table (id=1). Stores the current completion code
    that learners must enter to verify they completed the consent form.
    """

    __tablename__ = "consent_config"

    id = Column(Integer, primary_key=True)
    # Current completion code (displayed at end of JISC consent form)
    completion_code = Column(String, nullable=True, default=None)
    # Whether code verification is enabled
    code_required = Column(Boolean, nullable=False, default=False)


class ControllerStateModel(TimestampMixin, Base):
    """Persistent storage for controller state S_t (formal ARL)."""

    __tablename__ = "controller_states"

    id = Column(Integer, primary_key=True)
    learner_id = Column(
        String,
        ForeignKey("users.learner_id", ondelete="CASCADE"),
        unique=True,
        index=True,
        nullable=False,
    )
    mode = Column(String(32), nullable=False, default="nominal", index=True)
    state_version = Column(String(16), nullable=False, default="1.0.0")
    budgets_json = Column(Text, nullable=False)
    timers_json = Column(Text, nullable=False)
    recent_outcomes_json = Column(Text, nullable=False)
    metadata_json = Column(Text, nullable=True)

    user = relationship("User", backref="controller_state", uselist=False)


# -------------------------
# DB init/migrations
# -------------------------


def _get_table_columns(conn, table_name: str) -> set:
    """Get column names for a table using database-agnostic introspection."""
    try:
        inspector = inspect(conn)
        columns = inspector.get_columns(table_name)
        return {col["name"] for col in columns}
    except Exception:
        return set()


def _table_exists(conn, table_name: str) -> bool:
    """Check if a table exists using database-agnostic introspection."""
    try:
        inspector = inspect(conn)
        return table_name in inspector.get_table_names()
    except Exception:
        return False


def init_db():
    Base.metadata.create_all(bind=engine)

    # lightweight migrations for new sentiment tables — keep as no-ops if already present
    # Using database-agnostic introspection
    try:
        with engine.connect() as conn:
            # Verify tables exist (no-op check for backwards compatibility)
            for table in ["feedback", "sentiment_scores", "item_sentiment_agg", "learner_sentiment_window"]:
                _ = _get_table_columns(conn, table)
    except Exception:
        # Safe to ignore for fresh DBs
        pass

    # lightweight migration: add columns to clicks if missing (back-compat)
    try:
        with engine.begin() as conn:
            cols = _get_table_columns(conn, "clicks")
            if cols:  # Table exists
                from sqlalchemy import text
                if "source" not in cols:
                    conn.execute(text("ALTER TABLE clicks ADD COLUMN source TEXT"))
                if "rank" not in cols:
                    conn.execute(text("ALTER TABLE clicks ADD COLUMN rank INTEGER"))
                if "strategy" not in cols:
                    conn.execute(text("ALTER TABLE clicks ADD COLUMN strategy TEXT"))
                if "arm" not in cols:
                    conn.execute(text("ALTER TABLE clicks ADD COLUMN arm TEXT"))
                if "course_id" not in cols:
                    conn.execute(text("ALTER TABLE clicks ADD COLUMN course_id TEXT"))

            cols = _get_table_columns(conn, "mastery")
            if cols and "last_evidence_id" not in cols:
                conn.execute(text("ALTER TABLE mastery ADD COLUMN last_evidence_id INTEGER"))
    except Exception:
        # Safe to ignore on new schemas
        pass

    # lightweight migration: ensure telemetry metadata columns exist
    telemetry_columns = {
        "impressions": {
            "user_id": "INTEGER",
            "arm_key": "TEXT",
            "policy_version": "TEXT",
            "schema_version": "TEXT",
        },
        "clicks": {
            "user_id": "INTEGER",
            "arm_key": "TEXT",
            "policy_version": "TEXT",
            "schema_version": "TEXT",
        },
        "completions": {
            "user_id": "INTEGER",
            "arm_key": "TEXT",
            "policy_version": "TEXT",
            "schema_version": "TEXT",
        },
        "explanation_interactions": {
            "user_id": "INTEGER",
            "arm_key": "TEXT",
            "policy_version": "TEXT",
            "schema_version": "TEXT",
        },
        "reflections": {
            "user_id": "INTEGER",
            "arm_key": "TEXT",
            "policy_version": "TEXT",
            "schema_version": "TEXT",
        },
    }

    try:
        with engine.begin() as conn:
            from sqlalchemy import text
            for table, columns in telemetry_columns.items():
                existing = _get_table_columns(conn, table)
                if not existing:
                    continue
                for column, ddl in columns.items():
                    if column not in existing:
                        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}"))
    except Exception:
        # Safe to ignore on new schemas
        pass


def migrate_db():
    """Best-effort migration for impressions table and backfill from clicks."""
    try:
        with engine.begin() as conn:
            from sqlalchemy import text
            cols = _get_table_columns(conn, "impressions")
            if not cols:
                return  # Table doesn't exist yet

            if "request_id" not in cols:
                conn.execute(text("ALTER TABLE impressions ADD COLUMN request_id TEXT"))
            if "source" not in cols:
                conn.execute(text("ALTER TABLE impressions ADD COLUMN source TEXT"))
            if "rank" not in cols:
                conn.execute(text("ALTER TABLE impressions ADD COLUMN rank INTEGER"))
            if "course_id" not in cols:
                conn.execute(text("ALTER TABLE impressions ADD COLUMN course_id TEXT"))

            # Backfill any impressions stored in clicks table
            try:
                conn.execute(text(
                    "INSERT INTO impressions (learner_id, item_id, source, rank, strategy, arm, course_id, created_at) "
                    "SELECT learner_id, item_id, source, rank, strategy, arm, course_id, created_at FROM clicks WHERE action='impression'"
                ))
                conn.execute(text("DELETE FROM clicks WHERE action='impression'"))
            except Exception:
                pass
    except Exception:
        # Safe to ignore for fresh DBs
        pass


# -------------------------
# Experiment arm helpers
# -------------------------


_ARM_SEQUENCE = ["T", "A", "B"]


def _next_arm_round_robin(db) -> str:
    """Return the next arm in T, A, B order based on current assignment counts."""
    counts = {arm: 0 for arm in _ARM_SEQUENCE}
    for row in db.query(GroupAssignment.arm).all():
        if row.arm in counts:
            counts[row.arm] += 1
    # Pick the arm with the fewest assignments; ties go in T, A, B order
    return min(_ARM_SEQUENCE, key=lambda a: counts[a])


def deterministic_arm(learner_id: str) -> str:
    """Return the stored arm for a learner, or None if not yet assigned.

    Previously used a hash-based approach; now arms are assigned via
    round-robin so there is no deterministic mapping from learner_id alone.
    Falls back to looking up the persisted GroupAssignment.
    """
    db = SessionLocal()
    try:
        ga = db.query(GroupAssignment).filter_by(learner_id=learner_id).first()
        return ga.arm if ga else None
    finally:
        db.close()


def get_or_assign_arm(db, learner_id: str) -> str:
    ga = db.query(GroupAssignment).filter_by(learner_id=learner_id).first()
    if ga:
        return ga.arm
    arm = _next_arm_round_robin(db)
    seed = hashlib.sha256(learner_id.encode("utf-8")).hexdigest()
    ga = GroupAssignment(learner_id=learner_id, arm=arm, seed=seed)
    db.add(ga)
    db.commit()
    return arm


def set_arm(db, learner_id: str, arm: str) -> str:
    ga = db.query(GroupAssignment).filter_by(learner_id=learner_id).first()
    if ga:
        ga.arm = arm
    else:
        seed = hashlib.sha256(learner_id.encode("utf-8")).hexdigest()
        ga = GroupAssignment(learner_id=learner_id, arm=arm, seed=seed)
        db.add(ga)
    db.commit()
    return arm


# -------------------------
# App settings helpers
# -------------------------


def purge_sentiment_for_learner(db, learner_id: str) -> Dict[str, int]:
    """Remove reflections and sentiment aggregates for ``learner_id``.

    The function operates on the provided session without committing so that
    callers can bundle the purge with other writes (for example, recording the
    consent change).  A dictionary describing the number of rows deleted per
    table is returned for telemetry or auditing purposes.
    """

    stats: Dict[str, int] = {}

    stats["reflections"] = db.query(Reflection).filter(
        Reflection.learner_id == learner_id
    ).delete(synchronize_session=False)

    stats["sentiment_scores"] = db.query(SentimentScore).filter(
        SentimentScore.learner_id == learner_id
    ).delete(synchronize_session=False)

    stats["sentiment_aggregates"] = db.query(SentimentAggregate).filter(
        SentimentAggregate.learner_id == learner_id
    ).delete(synchronize_session=False)

    stats["sentiment_windows"] = 0
    window = db.query(LearnerSentimentWindow).filter(
        LearnerSentimentWindow.learner_id == learner_id
    ).one_or_none()
    if window is not None:
        db.delete(window)
        stats["sentiment_windows"] = 1

    return stats


# -------------------------
# Controller state helpers
# -------------------------


def get_controller_state(session: Session, learner_id: str):
    """Load controller state from database or initialize if missing.

    Returns a ControllerState instance from xelra.arl.controller_state.
    """
    from ..arl.controller_state import ControllerState, initialize_controller_state
    import json

    row = session.query(ControllerStateModel).filter_by(learner_id=learner_id).first()

    if row is None:
        state = initialize_controller_state(learner_id)
        save_controller_state(session, state)
        return state

    data = {
        "learner_id": row.learner_id,
        "mode": row.mode,
        "budgets": json.loads(row.budgets_json),
        "timers": json.loads(row.timers_json),
        "recent_outcomes": json.loads(row.recent_outcomes_json),
        "metadata": json.loads(row.metadata_json) if row.metadata_json else {},
        "version": row.state_version,
        "updated_at": row.updated_at.isoformat(),
    }

    return ControllerState.from_dict(data)


def save_controller_state(session: Session, state) -> None:
    """Persist controller state to database.

    Args:
        session: SQLAlchemy session
        state: ControllerState instance from xelra.arl.controller_state
    """
    import json

    row = session.query(ControllerStateModel).filter_by(learner_id=state.learner_id).first()

    state_dict = state.to_dict()

    if row is None:
        row = ControllerStateModel(
            learner_id=state.learner_id,
            mode=state.mode.value,
            state_version=state.version,
            budgets_json=json.dumps(state_dict["budgets"]),
            timers_json=json.dumps(state_dict["timers"]),
            recent_outcomes_json=json.dumps(state_dict["recent_outcomes"]),
            metadata_json=json.dumps(state_dict["metadata"]),
        )
        session.add(row)
    else:
        row.mode = state.mode.value
        row.state_version = state.version
        row.budgets_json = json.dumps(state_dict["budgets"])
        row.timers_json = json.dumps(state_dict["timers"])
        row.recent_outcomes_json = json.dumps(state_dict["recent_outcomes"])
        row.metadata_json = json.dumps(state_dict["metadata"])
        row.updated_at = state.updated_at

    session.flush()
