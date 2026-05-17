from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.agent import generate_response
import os
from app.rag import build_vector_db

port = int(os.environ.get("PORT", 8000))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

@app.get("/")
def home():
    return {"status": "ok", "message": "API is running"}