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