from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import generate_response
import os
from app.rag import build_vector_db

app = FastAPI()

if not os.path.exists("chroma_db"):
    build_vector_db()


# Request schema (IMPORTANT)
class ChatRequest(BaseModel):
    query: str


# Response schema
class ChatResponse(BaseModel):
    type: str
    message: str | None = None
    recommendations: list | None = None


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    result = generate_response(req.query)

    return {
        "type": result.get("type"),
        "message": result.get("message"),
        "recommendations": result.get("recommendations"),
    }