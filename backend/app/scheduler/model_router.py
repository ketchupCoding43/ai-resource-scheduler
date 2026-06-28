def select_model(predicted_class: str, predicted_score: float, metrics: dict) -> dict:
    gpu_metrics = metrics.get("gpu", {})
    memory_used_mb = gpu_metrics.get("memory_used_mb", 0)
    temperature_c = gpu_metrics.get("temperature_c", 0)

    vram_safe = memory_used_mb < 3500 and temperature_c < 80
    force_small = temperature_c > 83

    if predicted_class == "LIGHT":
        selected_model = "qwen2.5-coder:3b"
        routing_reason = "Light workload routed to fast draft model"
    elif predicted_class in {"MEDIUM", "HEAVY"}:
        if force_small:
            selected_model = "qwen2.5-coder:3b"
            routing_reason = "Forced 3B due to high temperature"
        elif vram_safe:
            selected_model = "qwen2.5-coder:7b"
            routing_reason = "Resources safe for stronger model"
        else:
            selected_model = "qwen2.5-coder:3b"
            routing_reason = "Resource fallback to draft model"
    else:
        selected_model = "qwen2.5-coder:3b" if vram_safe else "qwen2.5-coder:7b"
        routing_reason = "Fallback routing based on available resources"

    return {
        "selected_model": selected_model,
        "routing_reason": routing_reason,
        "vram_safe": vram_safe,
    }
