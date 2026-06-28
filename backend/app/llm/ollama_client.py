import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(
    prompt: str,
    model_name: str = "qwen2.5-coder:7b",
    context_size: int = 2048
):
    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": context_size
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=300
    )

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    response.raise_for_status()

    data = response.json()

    return {
        "response": data["response"],
        "model": data["model"]
    }
