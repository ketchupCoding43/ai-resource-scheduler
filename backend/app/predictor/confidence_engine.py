def evaluate_response_confidence(prompt: str, response: str, predicted_class: str) -> dict:
    prompt = prompt or ""
    response = response or ""

    prompt_words = [word.strip(".,!?;:()[]{}").lower() for word in prompt.split() if word.strip()]
    response_lower = response.lower()
    response_words = response_lower.split()

    confidence = 60
    reasons = []

    if len(response_words) < 20:
        confidence -= 20
        reasons.append("response too short")
    elif len(response_words) < 60:
        confidence += 5
        reasons.append("response length reasonable")
    else:
        confidence += 10
        reasons.append("response length strong")

    important_tokens = [
        token for token in prompt_words
        if len(token) > 4 and token not in {"explain", "detail", "details", "please", "about", "with"}
    ]
    if important_tokens:
        matched = sum(1 for token in important_tokens if token in response_lower)
        coverage = matched / len(important_tokens)
        if coverage >= 0.6:
            confidence += 15
            reasons.append("good prompt-response coverage")
        elif coverage >= 0.3:
            confidence += 5
            reasons.append("partial prompt-response coverage")
        else:
            confidence -= 10
            reasons.append("low prompt-response coverage")

    detail_terms = ["detail", "detailed", "architecture", "implementation", "internals"]
    if any(term in prompt.lower() for term in detail_terms) and len(response_words) < 40:
        confidence -= 15
        reasons.append("missing detail for detailed prompt")

    weak_phrases = ["i don't know", "cannot answer", "not sure", "i am not sure"]
    if any(phrase in response_lower for phrase in weak_phrases):
        confidence -= 20
        reasons.append("weak or uncertain response")

    if predicted_class == "HEAVY" and len(response_words) < 30:
        confidence -= 10
        reasons.append("heavy prompt with short response")

    confidence = max(0, min(100, confidence))
    if confidence >= 75:
        quality_class = "HIGH"
    elif confidence >= 50:
        quality_class = "MEDIUM"
    else:
        quality_class = "LOW"

    if not reasons:
        reasons.append("neutral confidence")

    return {
        "confidence": confidence,
        "quality_class": quality_class,
        "reasons": reasons,
    }
