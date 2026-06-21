def make_decision(
    workload_class: str,
    metrics: dict
):

    ram_usage = metrics["memory"]["usage_percent"]

    gpu_usage = metrics["gpu"]["usage_percent"]

    temperature = metrics["gpu"]["temperature_c"]

    # Critical RAM

    if ram_usage >= 95:
        return {
            "decision": "REJECT",
            "reason": "RAM usage above 95%"
        }

    # GPU overloaded

    if gpu_usage >= 90:
        return {
            "decision": "DELAY",
            "reason": "GPU usage above 90%"
        }

    # Temperature protection

    if temperature >= 80:
        return {
            "decision": "DELAY",
            "reason": "GPU temperature too high"
        }

    # Heavy workloads under pressure

    if (
        workload_class == "HEAVY"
        and ram_usage >= 85
    ):
        return {
            "decision": "DELAY",
            "reason": "Heavy workload during high RAM usage"
        }

    return {
        "decision": "EXECUTE",
        "reason": "Resources available"
    }