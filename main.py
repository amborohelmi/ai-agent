from fastapi import FastAPI
import requests
import os

app = FastAPI()

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-Coder-7B"

HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

def query(prompt):
    response = requests.post(API_URL, headers=headers, json={
        "inputs": prompt
    })
    return response.json()

@app.get("/")
def home():
    return {"status": "AI Agent Running 🚀"}

@app.post("/agent")
def agent(data: dict):
    prompt = data.get("prompt")
    result = query(prompt)
    return {"result": result}
