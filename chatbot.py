import os
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if api_key else None

SYSTEM_PROMPT = (
    "You are a compassionate mental health companion. Respond in a supportive, empathetic, "
    "and reassuring way. Keep your advice general, non-judgmental, and encourage self-care. "
    "If the user shares distress or crisis thoughts, remind them to seek immediate help from local "
    "emergency services or a trusted person."
)

# Fallback responses when API is unavailable
FALLBACK_RESPONSES = {
    "positive": [
        "That's wonderful! Keep nurturing that positive energy and continue doing what makes you feel good.",
        "I'm glad you're feeling good. Remember to share this joy with others and maintain these healthy habits.",
        "It's great to hear you're in a positive place. Keep building on this momentum!"
    ],
    "negative": [
        "I hear you're going through a tough time. Remember that it's okay to feel this way. Consider reaching out to someone you trust.",
        "Difficult emotions are a natural part of life. Be gentle with yourself and take things one step at a time.",
        "You deserve kindness, especially from yourself. Consider doing something small that brings you comfort today."
    ],
    "neutral": [
        "Thank you for sharing. It sounds like you're in a reflective space. Take time to understand what you're feeling.",
        "I'm here to listen. Feel free to share more about what's on your mind.",
        "Sometimes life feels balanced. That's okay. Is there anything specific you'd like to talk about?"
    ],
    "distress": [
        "I'm concerned about what you've shared. Please reach out to someone who can help—a trusted friend, family member, or professional.",
        "Your safety matters. If you're in crisis, please contact emergency services or a crisis hotline immediately.",
        "You don't have to face this alone. Please reach out for immediate support from those around you."
    ]
}


def get_fallback_response(sentiment: dict) -> str:
    """Return a rule-based response when OpenAI API is unavailable."""
    if sentiment["distress_alert"]:
        import random
        return random.choice(FALLBACK_RESPONSES["distress"])
    
    mood = sentiment.get("mood", "neutral")
    import random
    return random.choice(FALLBACK_RESPONSES.get(mood, FALLBACK_RESPONSES["neutral"]))


def generate_response(message: str, sentiment: dict) -> str:
    mood = sentiment.get("mood")
    extra_context = ""

    if sentiment["distress_alert"]:
        extra_context = (
            "The user may be in distress. Respond with calm, gentle support and suggest safe, grounding measures. "
            "Avoid sounding clinical."
        )
    elif mood == "negative":
        extra_context = (
            "The user seems to be feeling down. Offer empathy, encouragement, and a few small coping suggestions."
        )
    elif mood == "positive":
        extra_context = (
            "The user seems to be feeling positive. Reinforce their strength and encourage healthy habits."
        )

    prompt = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"{extra_context} User says: \"{message}\""},
    ]

    # If no API key or client not initialized, use fallback
    if not client:
        return get_fallback_response(sentiment)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.8,
            max_tokens=220,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        import sys
        import traceback
        print(f"ERROR in generate_response: {type(e).__name__}: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        logger.error(f"Error generating response: {e}", exc_info=True)
        # Fall back to rule-based response
        return get_fallback_response(sentiment)
