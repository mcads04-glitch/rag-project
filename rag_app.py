from pydantic import BaseModel
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

class QueryRequest(BaseModel):
     question: str 
     
def validate_user_input(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    if len(text) < 5:
        raise HTTPException(status_code=400, detail="Question is too short")

    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Question is too long")

def validate_model_output(text: str):
    if text is None or text.strip() == "":
        raise HTTPException(status_code=500, detail="AI returned an empty response")

    if len(text) < 10:
        raise HTTPException(status_code=500, detail="AI response is too short")

def review_model_output(original_answer: str):
    review_prompt = f"""
You are reviewing an AI-generated response.

Your job:
- If the response is unclear, incomplete, or poorly written, improve it.
- If the response is already good, return it unchanged.

AI response to review:
{original_answer}
"""

    review_model = genai.GenerativeModel("gemini-2.5-flash")
    review_response = review_model.generate_content(review_prompt)

    return review_response.text

    def validate_user_input(question: str):
        if question is None or question.strip() == "":
            raise HTTPException(status_code=400, detail="Question cannot be empty")
        if len(question) < 5:
            raise HTTPException(status_code=400, detail="Question is too short")
        if len(question) > 500:
            raise HTTPException(status_code=400, detail="Question is too long")

@app.post("/query")
def query_ai(request: QueryRequest):
    validate_user_input(request.question)
    primary_model = genai.GenerativeModel("gemini-2.5-flash")
    primary_response = primary_model.generate_content(request.question)
    raw_answer = primary_response.text
    print(f"Raw answer: {primary_response.text}")
    validate_model_output(raw_answer)
    reviewed_answer = review_model_output(raw_answer)
    print(f"Reviewed answer: {reviewed_answer}")
    return reviewed_answer
   



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
