import re

POSITIVE_WORDS = {
    "happy", "calm", "hopeful", "good", "positive", "relaxed", "grateful", "thankful", "joyful", "supported"
}
NEGATIVE_WORDS = {
    "sad", "anxious", "stress", "depressed", "lonely", "worried", "angry", "hopeless", "tired", "overwhelmed"
}
DISTRESS_KEYWORDS = {
    "suicide", "hurt", "self-harm", "die", "worthless", "can't", "cannot", "no one", "alone", "panic", "panic attack"
}


def normalize_text(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9\s]", "", text.lower())


def analyze_sentiment(message: str) -> dict:
    text = normalize_text(message)
    words = text.split()
    positives = sum(1 for word in words if word in POSITIVE_WORDS)
    negatives = sum(1 for word in words if word in NEGATIVE_WORDS)
    distress_hits = sum(1 for kw in DISTRESS_KEYWORDS if kw in text)

    polarity = positives - negatives
    intensity = 0
    if positives + negatives > 0:
        intensity = (positives - negatives) / (positives + negatives)

    distress_alert = distress_hits > 0 or intensity <= -0.5 or negatives >= 2

    if intensity >= 0.4:
        mood = "positive"
    elif intensity <= -0.3:
        mood = "negative"
    else:
        mood = "neutral"

    return {
        "mood": mood,
        "polarity": float(polarity),
        "intensity": float(intensity),
        "distress_alert": distress_alert,
        "distress_hits": int(distress_hits),
        "positives": int(positives),
        "negatives": int(negatives),
    }
