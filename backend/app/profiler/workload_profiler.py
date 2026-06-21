def classify_workload(
    latency_seconds: float,
    response_length: int
) -> str:

    if latency_seconds < 5:
        return "LIGHT"

    elif latency_seconds < 15:
        return "MEDIUM"

    else:
        return "HEAVY"