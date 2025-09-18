# consumer.py
import json
import time
from kafka import KafkaConsumer
import redis
from model_utils import extract_entities, analyze_sentiment

KAFKA_BOOTSTRAP = "localhost:9093"
TOPIC = "news.raw.en"
REDIS_URL = "redis://localhost:6379/0"

consumer = KafkaConsumer(TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP,
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         auto_offset_reset='earliest', enable_auto_commit=True)

r = redis.Redis.from_url(REDIS_URL)

def market_relevance(item):
    # simple heuristic: presence of company names/entities increases relevance
    txt = (item.get("title","") + " " + item.get("description","")).lower()
    keywords = ["earnings", "merger", "acquisition", "ipo", "sec", "rate"]
    score = 0.1
    for kw in keywords:
        if kw in txt:
            score += 0.2
    return min(score, 1.0)

def generate_signal(processed):
    # combine sentiment score and relevance into a numeric expected move
    impact = processed["sentiment"]["score"] * processed["relevance"]
    # signal object
    return {
        "symbol": processed.get("symbol"),  # in real world: map entities -> tickers
        "impact": impact,
        "confidence": abs(processed["sentiment"]["raw_score"]) * processed["relevance"],
        "timestamp": time.time(),
        "source": processed["source"],
        "title": processed["title"]
    }

for msg in consumer:
    item = msg.value
    text = (item.get("title","") + " " + item.get("description",""))
    entities = extract_entities(text)
    sent = analyze_sentiment(text)
    rel = market_relevance(item)
    processed = {"title": item.get("title"), "description": item.get("description"),
                 "entities": entities, "sentiment": sent, "relevance": rel, "source": item.get("source")}
    signal = generate_signal(processed)
    # store top signals in Redis sorted set by absolute impact
    key = "signals:hot"
    r.zadd(key, {json.dumps(signal): abs(signal["impact"])})
    # trim to top 200
    r.zremrangebyrank(key, 0, -201)
    print("Stored signal:", signal)

