import os

import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY is not set in .env")

genai.configure(api_key=api_key)
app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/generate-text")
def generate_text():
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        step1_prompt = "Write a three point outline for a short story about a cat."
        step1_response = model.generate_content(step1_prompt)

        step2_prompt = (
            "Using the three point outline below, write a short story about a cat.\n\n"
            f"{step1_response.text}"
        )
        step2_response = model.generate_content(step2_prompt)

        return {"status": "success", "text": step2_response.text}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate text")
