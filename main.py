from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

HF_TOKEN = os.getenv("HF_TOKEN")

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

class RequestBody(BaseModel):
    prompt: str

SYSTEM_PROMPT = """
You are an expert software engineer AI agent.
Give clean, structured, production-ready code.
"""

def call_qwen(prompt):
    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=60
    )

    # 🔥 INI YANG KAMU MAKSUD (RAW DEBUG)
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    try:
        data = response.json()
    except Exception:
        return {
            "error": "Non-JSON response from Hugging Face",
            "raw": response.text
        }

    if isinstance(data, dict) and "error" in data:
        return data

    return data[0]["generated_text"]

    return response.json()

@app.get("/")
def home():
    return {"status": "AI Agent Running"}

@app.post("/agent")
def agent(body: RequestBody):
    result = call_qwen(body.prompt)
    return {"result": result}
