def predictive_decision(
    predicted_class,
    metrics,
    queue_size
):

    gpu_usage = metrics["gpu"]["usage_percent"]

    if predicted_class == "HEAVY":

        if gpu_usage > 70:

            return {
                "decision": "DELAY",
                "reason": "Predicted heavy workload and GPU busy"
            }

    if queue_size > 5:

        return {
            "decision": "DELAY",
            "reason": "Queue congestion predicted"
        }

    return {
        "decision": "EXECUTE",
        "reason": "Resources available"
    }