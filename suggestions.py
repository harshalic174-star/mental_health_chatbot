def build_suggestions(sentiment: dict) -> list:
    mood = sentiment.get("mood")
    suggestions = []

    if sentiment["distress_alert"]:
        suggestions.append("Take a few slow, deep breaths and ground yourself by noticing your surroundings.")
        suggestions.append("Reach out to a trusted friend, family member, or mental health professional.")
        suggestions.append("If you feel unsafe, contact local emergency services right away.")
        return suggestions

    if mood == "negative":
        suggestions.extend([
            "Try writing down one small thing you are grateful for today.",
            "Take a short walk or stretch to release tension.",
            "Break tasks into smaller steps and be gentle with yourself.",
        ])
    elif mood == "positive":
        suggestions.extend([
            "Keep doing the things that help you feel balanced and calm.",
            "Share a positive moment with someone you trust.",
            "Continue practicing self-care, even when you feel okay.",
        ])
    else:
        suggestions.extend([
            "Check in with how your body feels and notice any tension.",
            "Try a simple breathing exercise to reset your emotions.",
            "If you want, talk more about what is on your mind.",
        ])

    return suggestions
