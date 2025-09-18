# model_utils.py
from transformers import pipeline
import spacy

nlp = spacy.load("en_core_web_sm")
sentiment = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

def extract_entities(text):
    doc = nlp(text)
    ents = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
    return ents

def analyze_sentiment(text):
    r = sentiment(text[:512])  # truncate
    # Map to 5-class stub: POSITIVE -> positive, NEGATIVE -> negative
    out = r[0]
    label = out["label"]
    score = float(out["score"])
    # Convert to -1..+1
    val = score if label.lower()=="positive" else -score
    return {"score": val, "label": label, "raw_score": score}
