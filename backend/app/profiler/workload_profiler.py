def classify_workload(prompt: str):

    prompt_lower = prompt.lower()

    technical_keywords = [
        "docker",
        "kubernetes",
        "api",
        "database",
        "python",
        "fastapi",
        "machine learning",
        "deep learning",
        "neural network",
        "llm",
        "transformer",
        "microservices",
        "networking",
        "security",
        "cloud"
    ]

    code_keywords = [
        "code",
        "implement",
        "function",
        "class",
        "algorithm",
        "debug",
        "script"
    ]

    tech_count = sum(
        1 for word in technical_keywords
        if word in prompt_lower
    )

    code_count = sum(
        1 for word in code_keywords
        if word in prompt_lower
    )

    prompt_length = len(prompt)

    score = (
        prompt_length * 0.2
        + tech_count * 10
        + code_count * 15
    )

    if score < 40:
        workload_class = "LIGHT"
    elif score < 80:
        workload_class = "MEDIUM"
    else:
        workload_class = "HEAVY"

    return {
        "score": round(score, 2),
        "class": workload_class
    }