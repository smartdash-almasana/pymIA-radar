from app.semantics.profile import load_profile

def deterministic_score(text: str) -> dict:
    profile = load_profile()
    normalized = text.lower()

    positive_hits = [
        term for term in profile.get("positive_signals", [])
        if term.lower() in normalized
    ]
    negative_hits = [
        term for term in profile.get("negative_signals", [])
        if term.lower() in normalized
    ]

    score = min(100, len(positive_hits) * 12)
    score = max(0, score - len(negative_hits) * 20)

    return {
        "score": score,
        "positive_hits": positive_hits,
        "negative_hits": negative_hits,
        "passes": score >= profile.get("minimum_deterministic_score", 20),
    }
