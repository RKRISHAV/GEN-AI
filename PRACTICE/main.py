from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import google.generativeai as genai
import os
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-flash-latest")

app = FastAPI()

# In-memory chat storage
chat_sessions: Dict[str, List[str]] = {}

# Bot roles
SYSTEM_PROMPTS = {
    "tutor": """
You are an expert AI tutor.
You explain concepts in simple words.
You use examples.
You avoid jargon.
You are concise but clear.
Never hallucinate facts.
""",

    "resume": """
You are a professional resume coach.
You give practical career advice.
You suggest improvements.
You focus on clarity and impact.
You are direct and honest.
""",

    "hr": """
You are an HR assistant.
You answer questions about hiring, interviews, and workplace behavior.
You are professional and neutral.
""",

    "legal": """
You are a legal document explainer.
You simplify legal language.
You do not give real legal advice.
You explain risks in plain English.
"""
}

class ChatRequest(BaseModel):
    session_id: str
    role: str
    message: str

class ChatResponse(BaseModel):
    reply: str
    timestamp: str
    session_id: str
    role: str

@app.get("/")
def home():
    return {"message": "GenAI Backend is running"}

@app.get("/roles")
def get_roles():
    return {"available_roles": list(SYSTEM_PROMPTS.keys())}

@app.delete("/clear/{session_id}")
def clear_session(session_id: str):
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return {"message": f"Session {session_id} cleared"}
    return {"message": "Session not found"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        session_id = request.session_id
        user_message = request.message
        role = request.role.lower()

        if role not in SYSTEM_PROMPTS:
            raise HTTPException(status_code=400, detail="Invalid role")

        if session_id not in chat_sessions:
            chat_sessions[session_id] = []

        chat_sessions[session_id].append(f"User: {user_message}")

        history = "\n".join(chat_sessions[session_id])
        system_prompt = SYSTEM_PROMPTS[role]

        full_prompt = system_prompt + "\n" + history + "\nAI:"

        response = model.generate_content(full_prompt)
        ai_reply = response.text

        chat_sessions[session_id].append(f"AI: {ai_reply}")

        return {
            "reply": ai_reply,
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "role": role
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
