import requests


OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_response(
    prompt: str,
    model: str = "qwen2.5-coder:7b"
):
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    response.raise_for_status()

    return response.json()