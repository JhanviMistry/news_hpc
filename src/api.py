# api.py
import json
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from database.connection import SessionLocal
from database.models import Signal

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = redis.Redis(host="localhost", port=6379, db=0)
db = SessionLocal()

@app.get("/signals/top")
def top_signals(n: int = 10):
    hot_key = "signals:hot"
    data_key = "signals:data"

    event_ids = r.zrevrange(
        hot_key,
        0,
        n - 1,
        withscores=True
    )

    results = []

    for event_id, score in event_ids:
        signal_json = r.hget(
            data_key,
            event_id
        )

        if signal_json is None:
            continue

        signal = json.loads(signal_json)

        results.append({
            "signal": signal,
            "score": score
        })

    return {
        "count": len(results),
        "signals": results
    }

@app.get("/signals/history")
def signal_history(limit: int = 20, offset: int = 0):
    rows = (
        db.query(Signal)
        .order_by(Signal.timestamp.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    total = db.query(Signal).count()

    return {
        "count": len(rows),
        "total": total,
        "limit": limit,
        "offset": offset,
        "signals": [
            {
                "id": signal.id,
                "event_id": signal.event_id,
                "symbol": signal.symbol,
                "title": signal.title,
                "source": signal.source,
                "impact": signal.impact,
                "confidence": signal.confidence,
                "confidence_level": signal.confidence_level,
                "event_type": signal.event_type,
                "timestamp": signal.timestamp,
                "relevance": signal.relevance,
                "sentiment_label": signal.sentiment_label,
                "sentiment_score": signal.sentiment_score,
                "entities": signal.entities,
            }
            for signal in rows
        ],
    }

@app.get("/signals/{signal_id}")
def get_signal(signal_id: int):
    signal = (
        db.query(Signal)
        .filter(Signal.id == signal_id)
        .first()
    )

    if signal is None:
        return {
            "error": "Signal not found"
        }

    return {
        "id": signal.id,
        "event_id": signal.event_id,
        "symbol": signal.symbol,
        "title": signal.title,
        "source": signal.source,
        "impact": signal.impact,
        "confidence": signal.confidence,
        "confidence_level": signal.confidence_level,
        "event_type": signal.event_type,
        "timestamp": signal.timestamp,
        "relevance": signal.relevance,
        "sentiment_label": signal.sentiment_label,
        "sentiment_score": signal.sentiment_score,
        "entities": signal.entities,
    }
