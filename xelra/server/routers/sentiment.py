"""Sentiment analysis routes for ad-hoc text and persisted learner reflections."""

import json
import logging
from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from ...models.sentiment.model import SentimentModel
from ...utils.db import Reflection, SessionLocal

logger = logging.getLogger(__name__)

router = APIRouter()

_sent_model = SentimentModel()


class TextIn(BaseModel):
    text: str


class ReflectionIn(BaseModel):
    learner_id: str
    text: str
    topic: Optional[str] = None
    item_id: Optional[str] = None
    prompt: Optional[str] = None
    reflection_id: Optional[int] = Field(default=None, alias="id")
    metadata: Optional[Any] = None


class SentimentBatchRequest(BaseModel):
    reflections: List[ReflectionIn]


class SentimentBatchResult(BaseModel):
    reflection_id: int
    learner_id: str
    topic: Optional[str]
    label: str
    confidence: float
    polarity: float


class SentimentBatchResponse(BaseModel):
    results: List[SentimentBatchResult]


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/sentiment/explain")
def sentiment_explain(body: TextIn):
    try:
        expl = _sent_model.explain_html(body.text)
    except Exception as e:  # pragma: no cover - runtime safety
        logger.exception("sentiment_explain failed")
        raise HTTPException(status_code=500, detail="Sentiment analysis failed")
    return {"ok": True, **expl}


@router.post("/sentiment/batch", response_model=SentimentBatchResponse)
def sentiment_batch(body: SentimentBatchRequest, db=Depends(get_db)):
    if not body.reflections:
        return SentimentBatchResponse(results=[])

    try:
        predictions = _sent_model.batch_predict([r.text for r in body.reflections])
    except Exception as e:  # pragma: no cover - runtime safety
        logger.exception("sentiment_batch prediction failed")
        raise HTTPException(status_code=500, detail="Sentiment analysis failed")

    pending = []
    for payload, pred in zip(body.reflections, predictions):
        topic = payload.topic.strip() if payload.topic else None
        reflection = None
        if payload.reflection_id is not None:
            reflection = (
                db.query(Reflection)
                .filter(Reflection.id == payload.reflection_id)
                .one_or_none()
            )

        if reflection is None:
            reflection = Reflection(
                learner_id=payload.learner_id,
                topic=topic,
                item_id=payload.item_id,
                prompt=payload.prompt,
                text=payload.text,
            )
            db.add(reflection)
        else:
            reflection.learner_id = payload.learner_id
            reflection.topic = topic
            reflection.item_id = payload.item_id
            reflection.prompt = payload.prompt
            reflection.text = payload.text

        reflection.sentiment = float(pred.get("polarity", 0.0))
        if payload.metadata is not None:
            try:
                reflection.metadata_json = json.dumps(payload.metadata)
            except TypeError:
                reflection.metadata_json = None
        pending.append((payload, pred, reflection))

    db.flush()

    results: List[SentimentBatchResult] = []
    for payload, pred, reflection in pending:
        results.append(
            SentimentBatchResult(
                reflection_id=int(reflection.id),
                learner_id=payload.learner_id,
                topic=reflection.topic,
                label=str(pred.get("label", "")),
                confidence=float(pred.get("confidence", 0.0)),
                polarity=float(pred.get("polarity", 0.0)),
            )
        )

    db.commit()

    return SentimentBatchResponse(results=results)
