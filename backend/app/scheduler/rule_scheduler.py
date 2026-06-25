def make_decision(workload_class, metrics, queue_size=0):

    ram_usage = metrics["memory"]["usage_percent"]

    gpu_temp = metrics["gpu"]["temperature_c"]

    if ram_usage > 85:
        return {
            "decision": "DELAY",
            "reason": "High RAM utilization"
        }

    if gpu_temp > 80:
        return {
            "decision": "DELAY",
            "reason": "GPU temperature too high"
        }

    if queue_size > 3:
        return {
            "decision": "DELAY",
            "reason": "Queue overloaded"
        }

    return {
        "decision": "EXECUTE",
        "reason": "Resources available"
    }