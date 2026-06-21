def classify_workload(
    prompt_length: int,
    response_length: int,
    latency_seconds: float,
    gpu_usage: float,
    vram_usage: float
):

    score = (
        prompt_length / 10
        + response_length / 50
        + latency_seconds
        + gpu_usage / 5
        + vram_usage / 500
    )

    if score < 30:
        workload_class = "LIGHT"

    elif score < 70:
        workload_class = "MEDIUM"

    else:
        workload_class = "HEAVY"

    return {
        "score": round(score, 2),
        "class": workload_class
    }