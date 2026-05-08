from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# =========================
# CORS (WAJIB supaya frontend jalan)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# ENV / TOKEN
# =========================
HF_TOKEN = os.getenv("HF_TOKEN")

# =========================
# MODEL (STABLE UNTUK API)
# =========================
API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen2.5-7B-Instruct"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

# =========================
# REQUEST BODY
# =========================
class RequestBody(BaseModel):
    prompt: str

# =========================
# AI CALL FUNCTION (ANTI ERROR VERSION)
# =========================
def call_ai(prompt: str):

    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=60
        )
    except Exception as e:
        return {"error": str(e)}

    # debug (lihat di Railway logs)
    print("STATUS:", response.status_code)
    print("TEXT:", response.text)

    # =========================
    # HANDLE ERROR HTTP
    # =========================
    if response.status_code != 200:
        return {
            "error": "Hugging Face API error",
            "status": response.status_code,
            "raw": response.text
        }

    # =========================
    # HANDLE JSON
    # =========================
    try:
        data = response.json()
    except Exception:
        return {
            "error": "Response not JSON",
            "raw": response.text
        }

    # =========================
    # HANDLE OUTPUT FORMAT
    # =========================
    try:
        return data[0]["generated_text"]
    except:
        return data


# =========================
# ROOT CHECK
# =========================
@app.get("/")
def home():
    return {"status": "AI Agent Running 🚀"}

# =========================
# MAIN AGENT ENDPOINT
# =========================
@app.post("/agent")
def agent(body: RequestBody):
    result = call_ai(body.prompt)
    return {"result": result}
