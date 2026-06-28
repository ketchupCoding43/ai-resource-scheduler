def should_escalate(confidence_result: dict, predicted_class: str, selected_model: str) -> dict:
    confidence = confidence_result.get("confidence", 0)

    if selected_model == "qwen2.5-coder:7b":
        return {
            "escalate": False,
            "target_model": None,
            "reason": "7B already selected",
        }

    if predicted_class in {"MEDIUM", "HEAVY"} and selected_model == "qwen2.5-coder:3b":
        return {
            "escalate": True,
            "target_model": "qwen2.5-coder:7b",
            "reason": "Predicted workload requires stronger model",
        }

    if selected_model == "qwen2.5-coder:3b" and confidence < 65:
        return {
            "escalate": True,
            "target_model": "qwen2.5-coder:7b",
            "reason": "Low confidence on draft response",
        }

    return {
        "escalate": False,
        "target_model": None,
        "reason": "Draft accepted",
    }
