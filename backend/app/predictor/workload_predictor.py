def predict_workload(prompt: str):

    prompt_length = len(prompt)

    score = 0

    score += prompt_length * 0.5

    prompt_lower = prompt.lower()

    heavy_keywords = [
        "explain",
        "architecture",
        "detailed",
        "report",
        "research",
        "compare",
        "analysis",
        "kubernetes",
        "machine learning",
        "deep learning"
    ]

    for keyword in heavy_keywords:
        if keyword in prompt_lower:
            score += 20

    if score < 40:
        workload_class = "LIGHT"

    elif score < 80:
        workload_class = "MEDIUM"

    else:
        workload_class = "HEAVY"

    return {
        "class": workload_class,
        "score": round(score, 2)
    }