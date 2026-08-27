# model_utils.py
from transformers import pipeline
import spacy
import re

nlp = spacy.load("en_core_web_sm")
sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def extract_entities(text):
    doc = nlp(text)

    entities = [
        {
            "text": ent.text,
            "label": ent.label_
        }
        for ent in doc.ents
    ]

    # Known financial entities
    known_companies = {
        "apple": "AAPL",
        "microsoft": "MSFT",
        "nvidia": "NVDA",
        "amazon": "AMZN",
        "alphabet": "GOOGL",
        "google": "GOOGL",
        "meta": "META",
        "tesla": "TSLA",
        "netflix": "NFLX",
        "home depot": "HD",
        "walmart": "WMT",
        "jpmorgan": "JPM",
        "jp morgan": "JPM",
        "goldman sachs": "GS",
        "bank of america": "BAC",
        "coca-cola": "KO",
        "pepsico": "PEP",
        "intel": "INTC",
        "amd": "AMD",
    }

    text_lower = text.lower()

    for company, ticker in known_companies.items():
        if re.search(
            rf"\b{re.escape(company)}\b",
            text_lower
        ):
            already_detected = any(
                entity["text"].lower() == company
                and entity["label"] == "ORG"
                for entity in entities
            )

            if not already_detected:
                entities.append({
                    "text": company.title(),
                    "label": "ORG",
                    "ticker": ticker
                })

    return entities

def analyze_sentiment(text):
    r = sentiment(text[:512])  # truncate
    # Map to 5-class stub: POSITIVE -> positive, NEGATIVE -> negative
    out = r[0]
    label = out["label"]
    score = float(out["score"])
    # Convert to -1..+1
    val = score if label.lower()=="positive" else -score
    return {"score": val, "label": label, "raw_score": score}
