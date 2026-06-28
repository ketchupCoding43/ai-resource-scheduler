def choose_context_size(prompt: str, selected_model: str, metrics: dict) -> dict:
    prompt = prompt or ""
    gpu_metrics = metrics.get("gpu", {})
    memory_used_mb = gpu_metrics.get("memory_used_mb", 0)
    temperature_c = gpu_metrics.get("temperature_c", 0)

    prompt_length = len(prompt)
    if temperature_c > 83:
        return {
            "context_size": 1024,
            "reason": "High temperature safety fallback",
        }

    if prompt_length < 120:
        return {
            "context_size": 1024,
            "reason": "Short prompt",
        }

    if prompt_length < 320:
        return {
            "context_size": 2048,
            "reason": "Medium prompt",
        }

    if selected_model == "qwen2.5-coder:3b" and memory_used_mb < 3500:
        return {
            "context_size": 4096,
            "reason": "Long prompt with safe 3B memory headroom",
        }

    if selected_model == "qwen2.5-coder:7b":
        if memory_used_mb < 3000:
            return {
                "context_size": 4096,
                "reason": "Long prompt and safe 7B memory headroom",
            }
        return {
            "context_size": 2048,
            "reason": "Default 7B context for safety",
        }

    return {
        "context_size": 2048,
        "reason": "Default context size",
    }
