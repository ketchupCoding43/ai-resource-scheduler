def select_model(predicted_class: str) -> str:
    if predicted_class == "LIGHT":
        return "qwen2.5-coder:3b"

    if predicted_class in {"MEDIUM", "HEAVY"}:
        return "qwen2.5-coder:7b"

    return "qwen2.5-coder:7b"
