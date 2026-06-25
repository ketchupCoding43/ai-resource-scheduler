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

    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    response.raise_for_status()

    data = response.json()

    return {
        "response": data["response"],
        "model": data["model"]
    }