# consumer.py
import json
import time
import hashlib
from signal_engine import detect_event, calculate_impact, calculate_confidence

from kafka import KafkaConsumer
from kafka import KafkaProducer
import redis

from sqlalchemy.exc import IntegrityError

from model_utils import extract_entities, analyze_sentiment
from database.connection import SessionLocal
from database.models import Signal

KAFKA_BOOTSTRAP = "localhost:9093"
TOPIC = "news.raw.en"
DLQ_TOPIC = "news.raw.en.dlq"
REDIS_URL = "redis://localhost:6379/0"

MAX_RETRIES = 3

consumer = KafkaConsumer(TOPIC, bootstrap_servers=KAFKA_BOOTSTRAP,
                         group_id="news-signal-processors",
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         auto_offset_reset='earliest', enable_auto_commit=False)

# producer inside the consumer cause
# consumer itself is responsible for forwarding failed messages
dlq_producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

r = redis.Redis.from_url(REDIS_URL)
db = SessionLocal()

def market_relevance(item):
    # simple heuristic: presence of company names/entities increases relevance
    txt = (item.get("title","") + " " + item.get("description","")).lower()
    keywords = ["earnings", "merger", "acquisition", "ipo", "sec", "rate"]
    score = 0.1
    for kw in keywords:
        if kw in txt:
            score += 0.2
    return min(score, 1.0)

# helper function to generate event id
# Idempotency - Every identical article gets the same hash
def generate_event_id(item):
    key = f"{item.get('source', '')}|{item.get('link', '')}"
    return hashlib.sha256(key.encode()).hexdigest()

def generate_signal(processed, event_id):
    impact = calculate_impact(
    processed["sentiment"]["score"],
    processed["relevance"],
    processed["event_type"]
    )

    confidence = calculate_confidence(
        processed["sentiment"]["raw_score"],
        processed["relevance"],
        processed["event_type"],
        processed["entities"]
    )

    return {
        "event_id": event_id,
        "symbol": processed.get("symbol"),
        "event_type": processed.get("event_type"),
        "impact": impact,
        #"confidence": abs(processed["sentiment"]["raw_score"]) * processed["relevance"],
        "confidence": confidence,
        "timestamp": time.time(),
        "source": processed["source"],
        "title": processed["title"]
    }

def send_to_dlq(item, error):
    payload = {
        "original_message": item,
        "error": str(error),
        "failed_at": time.time(),
    }

    dlq_producer.send(DLQ_TOPIC, payload)
    dlq_producer.flush()

    print("Sent message to DLQ.")

for msg in consumer:
    item = msg.value
    text = (item.get("title","") + " " + item.get("description",""))
    entities = extract_entities(text)
    sent = analyze_sentiment(text)
    rel = market_relevance(item)

    symbol = None

    for entity in entities:
        if entity.get("ticker"):
            symbol = entity["ticker"]
            break

    event_type = detect_event(text)

    processed = {
        "title": item.get("title"),
        "description": item.get("description"),
        "entities": entities,
        "symbol": symbol,
        "event_type": event_type,
        "sentiment": sent,
        "relevance": rel,
        "source": item.get("source")
    }
    event_id = generate_event_id(item)

    signal = generate_signal(
        processed,
        event_id
    )
    # store top signals in Redis sorted set by absolute impact
    '''
    key = "signals:hot"
    r.zadd(key, {json.dumps(signal): abs(signal["impact"])})
    # trim to top 200
    r.zremrangebyrank(key, 0, -201)
    print("Stored signal:", signal)
    '''

    # -------------------------
    # Redis: hot leaderboard
    # -------------------------
    key = "signals:hot"

    hot_key = "signals:hot"
    data_key = "signals:data"

    r.zadd(
        hot_key,
        {
            signal["event_id"]: abs(signal["impact"])
        }
    )

    r.hset(
        data_key,
        signal["event_id"],
        json.dumps(signal)
    )

    r.zremrangebyrank(
        hot_key,
        0,
        -201
    )


    # -------------------------
    # PostgreSQL: persistence
    # -------------------------
    db_signal = Signal(
        event_id=generate_event_id(item),
        symbol=signal.get("symbol"),
        title=signal["title"],
        source=signal["source"],
        impact=signal["impact"],
        confidence=signal["confidence"],
        timestamp=signal["timestamp"],
        relevance=processed["relevance"],
        sentiment_label=sent["label"],
        sentiment_score=sent["score"],
        entities=entities,
    )

    '''
    db.add(db_signal)
    db.commit()

    print("Stored signal:", signal)

    consumer.commit()
    '''

    success = False

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            #raise RuntimeError("Testing DLQ")
            db.add(db_signal)
            db.commit()

            success = True

            print(
                f"Stored signal successfully "
                f"(attempt {attempt}):",
                signal
            )

            break

        except IntegrityError:
            db.rollback()

            print("Duplicate article detected. Skipping.")

            success = True
            break

        except Exception as e:
            db.rollback()

            print(
                f"Database write failed "
                f"(attempt {attempt}/{MAX_RETRIES}): {e}"
            )

            time.sleep(2)

    if success:
        consumer.commit()
    else:
        send_to_dlq(item, "Max retries exceeded")
        consumer.commit()
