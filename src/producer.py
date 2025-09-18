# producer.py
import json
import time
from kafka import KafkaProducer
import requests
from bs4 import BeautifulSoup

KAFKA_BOOTSTRAP = "localhost:9093"
TOPIC = "news.raw.en"

producer = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def fetch_rss(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"RSS fetch failed: {e}")
        return []

    print(f"Fetched RSS content length: {len(r.content)}")   # 👈 add this
    soup = BeautifulSoup(r.content, "lxml-xml")
    items = []
    for item in soup.find_all("item")[:5]:
        items.append({
            "title": item.title.text if item.title else "",
            "description": item.description.text if item.description else "",
            "link": item.link.text if item.link else "",
            "source": url,
            "published": item.pubDate.text if item.pubDate else ""
        })
    print(f"Parsed {len(items)} items from {url}")           # 👈 add this
    return items

def fetch_json_stub(url):
    # Example of a JSON news source or social feed
    r = requests.get(url, timeout=10)
    data = r.json()
    # Expect data to be a list of messages
    return [ {"title": d.get("title",""), "description": d.get("text",""), "link": "", "source": url, "published": d.get("time","")} for d in data[:5] ]
    print(f"Fetched {len(data)} JSON items from {url}")

if __name__ == "__main__":
    rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"
    json_stub = "https://jsonplaceholder.typicode.com/posts"  # stub, not real news
    while True:
        items = fetch_rss(rss_url) + fetch_json_stub(json_stub)
        for it in items:
            producer.send(TOPIC, it)
        producer.flush()
        print(f"Published {len(items)} messages")
        time.sleep(60)
