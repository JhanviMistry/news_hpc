import re


EVENT_PATTERNS = {
    "earnings": [
        r"\bearnings\b",
        r"\bquarterly results\b",
        r"\bprofit\b",
        r"\brevenue\b",
        r"\bsales\b",
    ],

    "merger_acquisition": [
        r"\bmerger\b",
        r"\bacquisition\b",
        r"\bacquire\b",
        r"\bbuyout\b",
    ],

    "ipo": [
        r"\bipo\b",
        r"\bgo public\b",
        r"\bpublic offering\b",
    ],

    "regulatory": [
        r"\bsec\b",
        r"\bfda\b",
        r"\bregulator\b",
        r"\bregulators\b",
        r"\bapproval\b",
        r"\bapproved\b",
        r"\bfine\b",
        r"\bpenalty\b",
    ],

    "leadership": [
        r"\bceo\b",
        r"\bchief executive\b",
        r"\bresigns\b",
        r"\bresigned\b",
        r"\bappointed\b",
        r"\bsteps down\b",
    ],

    "product": [
        r"\bproduct launch\b",
        r"\blaunches\b",
        r"\brecall\b",
        r"\brecalled\b",
    ],

    "macro": [
        r"\binterest rate\b",
        r"\brates\b",
        r"\binflation\b",
        r"\bfederal reserve\b",
        r"\bfed\b",
    ],
}

EVENT_WEIGHTS = {
    "merger_acquisition": 1.5,
    "earnings": 1.3,
    "regulatory": 1.4,
    "leadership": 1.2,
    "macro": 1.3,
    "ipo": 1.4,
    "product": 1.1,
    "general": 0.7,
}


def detect_event(text):
    """
    Detect the most relevant financial event in an article.
    """

    text_lower = text.lower()

    detected = []

    for event_type, patterns in EVENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text_lower):
                detected.append(event_type)
                break

    if not detected:
        return "general"

    return detected[0]

def calculate_impact(sentiment_score, relevance, event_type):
    """
    Calculate market impact using sentiment, relevance,
    and the type of financial event.
    """

    event_weight = EVENT_WEIGHTS.get(event_type, 0.7)

    impact = (
        sentiment_score
        * relevance
        * event_weight
    )

    # Keep impact within -1 to +1
    return max(-1.0, min(1.0, impact))