import json
import requests

LLM_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:14b"


def ask_llm_json(prompt: str) -> dict:
    response = requests.post(
        LLM_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )
    response.raise_for_status()
    data = response.json()

    text = data["response"].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start:end+1])
        raise ValueError(f"LLM did not return valid JSON: {text}")