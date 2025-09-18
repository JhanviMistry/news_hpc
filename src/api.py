# api.py
import json
import redis
from fastapi import FastAPI
from typing import List

app = FastAPI()
r = redis.Redis(host="localhost", port=6379, db=0)

@app.get("/signals/top")
def top_signals(n: int = 10):
    key = "signals:hot"
    # get highest scores (reverse)
    items = r.zrevrange(key, 0, n-1, withscores=True)
    results = []
    for bs, score in items:
        results.append({"signal": json.loads(bs), "score": score})
    return {"count": len(results), "signals": results}
