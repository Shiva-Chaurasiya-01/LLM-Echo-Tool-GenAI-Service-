from pydantic import BaseModel
from fastapi import FastAPI, Form
from google import genai
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

app = FastAPI()

api_key = os.getenv("GEMINI_API_KEY")
model = os.getenv("GEMINI_MODEL")

client = genai.Client(api_key=api_key)


class RewriteRequest(BaseModel):
    text: str
    mood: Optional[str] = "Professional"
    language: Optional[str] = "English"


class RewriteResponse(BaseModel):
    text: str


@app.post("/rewrite", response_model=RewriteResponse)
async def rewrite(
    text: str = Form(...),
    mood: str = Form("Professional"),
    language: str = Form("English")
):
    if not text.strip():
        return {"text": "Please provide some text for us to rewrite"}

    mood_map = {
        "Professional": "polite and professional",
        "Casual": "casual and friendly",
        "Formal": "formal and respectful",
        "Friendly": "warm and friendly",
        "Creative": "creative and engaging"
    }
    
    tone = mood_map.get(mood, "polite and professional")
    
    prompt = f"""
Rewrite the following text in a {tone} tone.
Do not be aggressive.
Do not change the original meaning.
Keep the result concise.
Return only rewritten text.
Write the response in {language}.

Text:
{text}
"""
    
    try:
        response = client.models.generate_content(model=model, contents=prompt)
        return {"text": response.text.strip()}

    except Exception as e:
        return {"text": f"AI service Failed. Please try again later. Error: {str(e)}"}
