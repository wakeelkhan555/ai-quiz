import requests

def generate_fun_fact(question):

    prompt = f"""
    You are a helpful educational assistant.

    The quiz question is: {question}

    Generate one interesting, educational fun fact related to this question.
    Keep it to 2 short sentences.
    Avoid making up statistics or unsupported claims.
    Return only the fun fact.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:3b",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"].strip()


fact = generate_fun_fact("What is the capital of France?")

print("\nAI Fun Fact:")
print(fact)