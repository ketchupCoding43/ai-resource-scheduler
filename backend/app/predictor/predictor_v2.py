from app.predictor.feature_extractor import extract_features


def _base_score(features: dict) -> float:
    score = 0.0
    score += features.get("prompt_length", 0) * 0.04
    score += features.get("word_count", 0) * 0.35
    score += features.get("sentence_count", 1) * 0.5
    score += features.get("question_count", 0) * 0.5
    score += features.get("technical_keyword_count", 0) * 3
    score += features.get("code_keyword_count", 0) * 4
    score += features.get("topic_count", 0) * 5
    score += features.get("semantic_score", 0) * 0.6
    score += features.get("complexity_score", 0) * 0.25
    score += features.get("technical_domain_score", 0) * 0.15
    score += features.get("complexity_term_score", 0) * 0.2

    intent = features.get("intent", "GENERAL")
    response_size = features.get("expected_response_size", "MEDIUM")

    score += {
        "DEFINE": 0,
        "EXPLAIN": 10,
        "COMPARE": 12,
        "ARCHITECTURE": 20,
        "CODE_GENERATION": 24,
        "DEBUGGING": 14,
        "TUTORIAL": 18,
        "ANALYSIS": 16,
        "GENERAL": 0,
    }.get(intent, 0)

    score += {
        "SMALL": 0,
        "MEDIUM": 4,
        "LARGE": 8,
    }.get(response_size, 4)

    return score


def predict_workload_v2(prompt):
    features = extract_features(prompt)

    complexity_score = features["complexity_score"]
    score = complexity_score + _base_score(features) * 0.15

    if complexity_score < 25:
        workload_class = "LIGHT"
    elif complexity_score < 60:
        workload_class = "MEDIUM"
    else:
        workload_class = "HEAVY"

    confidence = 55.0

    if workload_class == "LIGHT":
        confidence += max(0, 25 - complexity_score) * 1.2
    elif workload_class == "MEDIUM":
        confidence += max(0, 20 - abs(42 - complexity_score)) * 1.4
    else:
        confidence += max(0, complexity_score - 60) * 0.8

    intent = features["intent"]
    response_size = features["expected_response_size"]

    confidence += min(15, complexity_score / 10)
    confidence += 6 if intent != "GENERAL" else 0
    confidence += 6 if response_size == "LARGE" else 0

    confidence = round(min(confidence, 99.0), 2)

    return {
        "class": workload_class,
        "score": round(complexity_score, 2),
        "confidence": confidence,
        "intent": intent,
        "expected_response_size": response_size,
        "complexity_score": complexity_score,
        "features": features,
    }
