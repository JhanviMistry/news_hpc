# api.py
import json
import redis
from fastapi import FastAPI
from typing import List

from src.database.connection import SessionLocal
from src.database.models import Signal

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=0)
db = SessionLocal()

@app.get("/signals/top")
def top_signals(n: int = 10):
    key = "signals:hot"
    # get highest scores (reverse)
    items = r.zrevrange(key, 0, n-1, withscores=True)
    results = []
    for bs, score in items:
        results.append({"signal": json.loads(bs), "score": score})
    return {"count": len(results), "signals": results}

@app.get("/signals/history")
def signal_history(limit: int = 20):
    rows = (
        db.query(Signal)
        .order_by(Signal.timestamp.desc())
        .limit(limit)
        .all()
    )

    return {
        "count": len(rows),
        "signals": [
            {
                "id": signal.id,
                "symbol": signal.symbol,
                "title": signal.title,
                "source": signal.source,
                "impact": signal.impact,
                "confidence": signal.confidence,
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
        "symbol": signal.symbol,
        "title": signal.title,
        "source": signal.source,
        "impact": signal.impact,
        "confidence": signal.confidence,
        "timestamp": signal.timestamp,
        "relevance": signal.relevance,
        "sentiment_label": signal.sentiment_label,
        "sentiment_score": signal.sentiment_score,
        "entities": signal.entities,
    }
