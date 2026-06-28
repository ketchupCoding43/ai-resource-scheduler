def make_final_decision(
    predicted_class,
    predicted_score,
    context_size,
    before_metrics,
    selected_model
):
    ram_usage = before_metrics["memory"]["usage_percent"]
    gpu_temp = before_metrics["gpu"]["temperature_c"]
    vram_used = before_metrics["gpu"]["memory_used_mb"]
    vram_total = before_metrics["gpu"].get("memory_total_mb") or 0
    gpu_usage = before_metrics["gpu"]["usage_percent"]
    prompt_pressure = 0

    if predicted_class == "HEAVY":
        prompt_pressure += 3
    elif predicted_class == "MEDIUM":
        prompt_pressure += 2
    else:
        prompt_pressure += 1

    if predicted_score >= 70:
        prompt_pressure += 2
    elif predicted_score >= 45:
        prompt_pressure += 1

    if context_size >= 4096:
        prompt_pressure += 2
    elif context_size >= 2048:
        prompt_pressure += 1

    if ram_usage > 90:
        return {
            "decision": "DELAY",
            "reason": "RAM usage is above 90%, so execution should wait.",
            "risk_level": "HIGH",
        }

    if gpu_temp > 83:
        if selected_model == "qwen2.5-coder:7b":
            return {
                "decision": "DOWNGRADE",
                "reason": "GPU temperature is high, so downgrade to 3B or delay.",
                "risk_level": "HIGH",
            }

        return {
            "decision": "DELAY",
            "reason": "GPU temperature is high, so execution should wait.",
            "risk_level": "HIGH",
        }

    vram_headroom = max(vram_total - vram_used, 0)
    vram_pressure = 0

    if vram_total:
        vram_used_percent = (vram_used / vram_total) * 100
        if vram_used_percent >= 85:
            vram_pressure = 3
        elif vram_used_percent >= 70:
            vram_pressure = 2
        elif vram_used_percent >= 50:
            vram_pressure = 1
    elif vram_used > 0:
        if vram_used > 12000:
            vram_pressure = 3
        elif vram_used > 8000:
            vram_pressure = 2
        elif vram_used > 4000:
            vram_pressure = 1

    if selected_model == "qwen2.5-coder:7b" and vram_pressure >= 2:
        return {
            "decision": "DOWNGRADE",
            "reason": "7B is likely to stress VRAM, so downgrade to 3B.",
            "risk_level": "HIGH",
        }

    if predicted_class == "HEAVY" and ram_usage <= 85 and gpu_temp <= 83 and (not vram_total or vram_headroom > 0):
        return {
            "decision": "EXECUTE",
            "reason": "Heavy workload with safe resources can run on 7B.",
            "risk_level": "MEDIUM",
        }

    if predicted_class == "MEDIUM" and context_size >= 4096:
        if vram_pressure <= 1 and gpu_usage <= 80:
            return {
                "decision": "EXECUTE",
                "reason": "Medium workload with large context can use 7B safely.",
                "risk_level": "MEDIUM",
            }
        return {
            "decision": "DOWNGRADE",
            "reason": "Medium workload needs a safer model because VRAM headroom is limited.",
            "risk_level": "MEDIUM",
        }

    if predicted_class == "LIGHT" and context_size <= 2048:
        return {
            "decision": "EXECUTE",
            "reason": "Light workload with compact context should run on 3B.",
            "risk_level": "LOW",
        }

    if predicted_class == "LIGHT" and (context_size > 2048 or predicted_score >= 35):
        return {
            "decision": "ESCALATE",
            "reason": "Light prompt has high latency or context pressure, so escalate to 7B.",
            "risk_level": "MEDIUM",
        }

    if predicted_score >= 60 or prompt_pressure >= 5:
        return {
            "decision": "EXECUTE",
            "reason": "Prompt complexity and resources support a 7B execution.",
            "risk_level": "MEDIUM",
        }

    if prompt_pressure <= 2:
        return {
            "decision": "EXECUTE",
            "reason": "Prompt and runtime pressure are low enough for execution.",
            "risk_level": "LOW",
        }

    return {
        "decision": "DELAY",
        "reason": "Resource signals are mixed, so delay to reduce execution risk.",
        "risk_level": "MEDIUM",
    }
