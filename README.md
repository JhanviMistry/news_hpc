# Real-time Financial News Sentiment Analysis (LLM)

This project is a real-time streaming pipeline that ingests financial news, extracts key entities, analyzes sentiment using LLMs, and generates actionable market signals. It is designed as a prototype for High-Performance Computing (HPC) + AI in finance, simulating how large-scale distributed systems can process market-moving news in real time.

Features

- **Producer** : Scrapes live RSS feeds (e.g., NYTimes Business) and publishes news to Apache Kafka.
- **Consumer** : Subscribes to Kafka topics, performs:
    - Name Entity Recognition (NER) using spaCy
    - Sentiment analysis using transformer-based LLM
    - Market relevance scoring with heuristics

- **Signal Engine** : Generates numerical signals combining sentiment + relevance → stored in Redis as ranked signals.

- **Scalable Architecture** : Kafka (streaming), Redis (fast storage), Docker Compose (multi-service orchestration).

- **HPC Angle** : The modular design allows scaling Kafka partitions, Redis clusters, and distributed model inference for high-throughput financial analytics.

---

## 🏗 Architecture

[RSS/News Feeds] → [Producer.py] → [Kafka Topic: news.raw.en] → [Consumer.py + LLM + NER] → [Redis Sorted Set] → [Signals Dashboard]



- **Producer**: Scrapes financial news from RSS feeds and publishes to Kafka.  
- **Consumer**: Subscribes to Kafka, classifies sentiment with **FinBERT**, and pushes results to Redis & ClickHouse.  
- **Hot Storage**: Redis stores top-N “hot” signals for fast queries.  
- **Warm Storage**: ClickHouse stores full history for analytics.  

---

## ⚡ Technologies

Tech Stack

Python (data pipeline, NLP, LLM inference)
Apache Kafka (real-time messaging)
Redis (fast ranking of signals)
spaCy (entity extraction)
Hugging Face Transformers (sentiment analysis)
Docker Compose (Kafka + Redis orchestration)pipeline.  

---

## 🚀 Running the Prototype

### 1. Clone the repo
```bash
git clone https://github.com/JhanviMistry/news_hpc.git
cd news_hpc
```
### 2. Start the Service

```bash
docker-compose up -d
```
### 3. Create and activate Python environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Download spaCy model
```bash
python -m spacy download en_core_web_sm
```

### 5. Run the producer
```bash
python src/producer.py
```

### 6. Run the consumer
```bash
python src/consumer.py
```
### 7. OPen the link for the output
http://localhost:9093

