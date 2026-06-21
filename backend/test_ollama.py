from app.llm.ollama_client import generate_response

response = generate_response(
    "Explain what is CPU scheduling in simple words."
)

print(response["response"])