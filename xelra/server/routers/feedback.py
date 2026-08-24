"""Feedback routes with sentiment scoring and rolling aggregate updates."""

import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import datetime as dt
from sqlalchemy import func
from ...utils.db import (
    SessionLocal,
    Feedback,
    SentimentScore,
    ItemSentimentAgg,
    LearnerSentimentWindow,
)
from ...utils.sentiment import analyse as analyse_sent
from ...models.sentiment.model import SentimentModel

logger = logging.getLogger(__name__)

router = APIRouter()

_sent_xai_model = SentimentModel()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class FeedbackIn(BaseModel):
    learner_id: str
    item_id: str
    text: str
    rating: int | None = None


@router.post("/feedback")
def submit_feedback(body: FeedbackIn, db=Depends(get_db)):
    fb = (
        db.query(Feedback)
        .filter_by(learner_id=body.learner_id, item_id=body.item_id)
        .first()
    )
    text_clean = (body.text or "").strip()

    if fb:
        # Only overwrite text if a real reflection was provided
        if text_clean:
            fb.text = body.text
        if body.rating is not None:
            fb.rating = body.rating
        fb.created_at = dt.datetime.now(dt.timezone.utc)
    else:
        fb = Feedback(
            learner_id=body.learner_id,
            item_id=body.item_id,
            text=body.text if text_clean else "",
            rating=body.rating,
        )
        db.add(fb)

    # Always commit the feedback record
    db.commit()

    # Compute sentiment only when there is non-empty text
    if text_clean:
        try:
            p, c = _sent_xai_model.score_confidence(body.text)
        except Exception:
            logger.warning("Sentiment model failed for item=%s, using heuristic", body.item_id)
            p, c = analyse_sent(body.text)
        ss = SentimentScore(
            learner_id=body.learner_id, item_id=body.item_id, polarity=p, confidence=c
        )
        db.add(ss)
        db.commit()

        # update item aggregate
        rows = db.query(SentimentScore).filter_by(item_id=body.item_id).all()
        if rows:
            vals = [r.polarity for r in rows]
            mu = sum(vals) / len(vals)
            st = (
                (sum((v - mu) ** 2 for v in vals) / len(vals)) ** 0.5
                if len(vals) > 1
                else 0.0
            )
            agg = db.query(ItemSentimentAgg).filter_by(item_id=body.item_id).first()
            if not agg:
                agg = ItemSentimentAgg(
                    item_id=body.item_id,
                    mean_polarity=mu,
                    n=len(vals),
                    stdev=st,
                    updated_at=dt.datetime.now(dt.timezone.utc),
                )
                db.add(agg)
            else:
                agg.mean_polarity = mu
                agg.n = len(vals)
                agg.stdev = st
                agg.updated_at = dt.datetime.now(dt.timezone.utc)
            db.commit()

        # update learner 7d window
        cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=7)
        rows = (
            db.query(SentimentScore)
            .filter(
                SentimentScore.learner_id == body.learner_id,
                SentimentScore.created_at >= cutoff,
            )
            .all()
        )
        if rows:
            vals = [r.polarity for r in rows]
            mu = sum(vals) / len(vals)
            win = (
                db.query(LearnerSentimentWindow)
                .filter_by(learner_id=body.learner_id)
                .first()
            )
            if not win:
                win = LearnerSentimentWindow(
                    learner_id=body.learner_id,
                    mean_polarity_7d=mu,
                    n_7d=len(vals),
                    updated_at=dt.datetime.now(dt.timezone.utc),
                )
                db.add(win)
            else:
                win.mean_polarity_7d = mu
                win.n_7d = len(vals)
                win.updated_at = dt.datetime.now(dt.timezone.utc)
            db.commit()
    else:
        # No text → no sentiment stored/scored
        p, c = 0.0, 0.0
        db.commit()

    return {
        "ok": True,
        "polarity": p,
        "confidence": c,
    }


@router.get("/feedback/latest_explain/{learner_id}")
def latest_feedback_explain(learner_id: str, db=Depends(get_db)):
    empty = {"tokens": [], "weightsPos": [], "weightsNeg": []}

    # Prefer the latest non-empty reflection by using SentimentScore timestamps
    ss = (
        db.query(SentimentScore)
        .filter(SentimentScore.learner_id == learner_id)
        .order_by(SentimentScore.created_at.desc())
        .first()
    )
    if ss:
        fb = (
            db.query(Feedback)
            .filter(
                Feedback.learner_id == learner_id,
                Feedback.item_id == ss.item_id,
                Feedback.text.isnot(None),
                func.length(func.trim(Feedback.text)) > 0,
            )
            .first()
        )
        if fb:
            lime = empty
            shap = empty
            try:
                expl_tok = _sent_xai_model.explain_tokens(fb.text)
                lime = expl_tok.get("lime", empty)
                shap = expl_tok.get("shap", empty)
            except Exception:
                pass
            return {
                "ok": True,
                "text": fb.text,
                "polarity": float(ss.polarity or 0.0),
                "confidence": float(ss.confidence or 0.0),
                "lime": lime,
                "shap": shap,
            }

    # Fallback: previous behaviour (latest Feedback row that has non-empty text)
    fb = (
        db.query(Feedback)
        .filter(
            Feedback.learner_id == learner_id,
            Feedback.text.isnot(None),
            func.length(func.trim(Feedback.text)) > 0,
        )
        .order_by(Feedback.created_at.desc())
        .first()
    )
    if not fb:
        return {
            "ok": True,
            "text": None,
            "lime": empty,
            "shap": empty,
            "polarity": 0.0,
            "confidence": 0.0,
        }
    try:
        p, c = _sent_xai_model.score_confidence(fb.text)
    except Exception:
        logger.warning("Sentiment model failed for latest_explain, using heuristic")
        p, c = analyse_sent(fb.text)
    lime = empty
    shap = empty
    try:
        expl_tok = _sent_xai_model.explain_tokens(fb.text)
        lime = expl_tok.get("lime", empty)
        shap = expl_tok.get("shap", empty)
    except Exception:
        pass
    return {
        "ok": True,
        "text": fb.text,
        "polarity": p,
        "confidence": c,
        "lime": lime,
        "shap": shap,
    }
