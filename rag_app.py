import google.generativeai as genai
from fastapi import FastAPI
app = FastAPI()
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/generate-text")
def generate_text():
     prompt = "Write a short story about a cat."
     model = genai.GenerativeModel("gemini-2.5-flash")
     response = model.generate_content(prompt)
     print(response)
     return{"text": response.text}