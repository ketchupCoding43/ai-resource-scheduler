def select_model(
    predicted_class: str,
    cpu_usage: float = 0,
    ram_usage: float = 0,
    gpu_usage: float = 0,
):
    """
    Select the most suitable model based on
    predicted workload and current resources.
    """

    # LIGHT workloads
    if predicted_class == "LIGHT":
        return {
            "model": "qwen2.5-coder:3b",
            "reason": "Light workload predicted"
        }

    # MEDIUM workloads
    elif predicted_class == "MEDIUM":

        # If resources are busy, use smaller model
        if cpu_usage > 80 or ram_usage > 80 or gpu_usage > 80:
            return {
                "model": "qwen2.5-coder:3b",
                "reason": "Medium workload but resources are busy"
            }

        return {
            "model": "qwen2.5-coder:7b",
            "reason": "Medium workload and resources available"
        }

    # HEAVY workloads
    elif predicted_class == "HEAVY":
        return {
            "model": "qwen2.5-coder:7b",
            "reason": "Heavy workload predicted"
        }

    # Fallback
    return {
        "model": "qwen2.5-coder:3b",
        "reason": "Fallback model"
    }