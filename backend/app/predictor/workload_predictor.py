from app.predictor.feature_extractor import extract_features


def predict_workload(prompt: str):
    features = extract_features(prompt)

    score = 0.0
    score += features["prompt_length"] * 0.08
    score += features["word_count"] * 0.5
    score += features["technical_keyword_count"] * 2
    score += features["code_keyword_count"] * 3
    score += features["topic_count"] * 3
    score += features["semantic_score"] * 0.45

    if score < 25:
        workload_class = "LIGHT"
    elif score < 60:
        workload_class = "MEDIUM"
    else:
        workload_class = "HEAVY"

    return {
        "class": workload_class,
        "score": round(score, 2),
    }
