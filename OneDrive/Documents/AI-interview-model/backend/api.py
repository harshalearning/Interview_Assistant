"""Backend module for API endpoints and orchestration."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import uuid
from datetime import datetime

from config import settings
from llm.models import OllamaClient, InterviewQuestionGenerator

# Router for backend endpoints
router = APIRouter(prefix="/api/v1", tags=["backend"])

ollama_client = OllamaClient(base_url=settings.ollama_base_url)
question_generator = InterviewQuestionGenerator()

# Models
class InterviewQuestion(BaseModel):
    """Model for interview question."""
    id: Optional[str] = None
    question: str
    topic: str
    difficulty: str = "medium"
    created_at: Optional[str] = None

class InterviewResponse(BaseModel):
    """Model for user response to interview question."""
    question_id: str
    response_text: str
    audio_url: Optional[str] = None
    confidence_score: Optional[float] = None

class InterviewSession(BaseModel):
    """Model for interview session."""
    id: Optional[str] = None
    user_id: str
    topic: str
    questions: List[InterviewQuestion] = []
    responses: List[InterviewResponse] = []
    status: str = "active"  # active, completed, paused
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class QuestionGenerationRequest(BaseModel):
    """Request payload for interview question generation."""
    topic: str
    difficulty: str = "medium"
    model: Optional[str] = None

class QuestionGenerationResponse(BaseModel):
    """Response payload for interview question generation."""
    question: str
    source: str
    model: Optional[str] = None
    fallback_used: bool = False

# In-memory session storage (replace with database later)
sessions: dict = {}

@router.post("/sessions/create", response_model=InterviewSession)
async def create_session(user_id: str, topic: str):
    """Create a new interview session."""
    session_id = str(uuid.uuid4())
    session = InterviewSession(
        id=session_id,
        user_id=user_id,
        topic=topic,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat()
    )
    sessions[session_id] = session.dict()
    return session

@router.get("/sessions/{session_id}", response_model=InterviewSession)
async def get_session(session_id: str):
    """Retrieve a session by ID."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    return InterviewSession(**sessions[session_id])

@router.post("/sessions/{session_id}/questions/add")
async def add_question(session_id: str, question: InterviewQuestion):
    """Add a question to a session."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    question.id = str(uuid.uuid4())
    question.created_at = datetime.utcnow().isoformat()
    
    sessions[session_id]["questions"].append(question.dict())
    return {"status": "added", "question_id": question.id}

@router.post("/sessions/{session_id}/responses/submit")
async def submit_response(session_id: str, response: InterviewResponse):
    """Submit a response to a question."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions[session_id]["responses"].append(response.dict())
    sessions[session_id]["updated_at"] = datetime.utcnow().isoformat()
    
    return {"status": "recorded", "response_id": str(uuid.uuid4())}

@router.patch("/sessions/{session_id}/status")
async def update_session_status(session_id: str, status: str):
    """Update session status."""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    valid_statuses = ["active", "completed", "paused"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
    
    sessions[session_id]["status"] = status
    sessions[session_id]["updated_at"] = datetime.utcnow().isoformat()
    
    return {"status": "updated", "new_status": status}

@router.get("/sessions")
async def list_sessions(user_id: Optional[str] = None):
    """List all sessions or filter by user_id."""
    if user_id:
        return [s for s in sessions.values() if s["user_id"] == user_id]
    return list(sessions.values())

@router.post("/llm/generate-question", response_model=QuestionGenerationResponse)
async def generate_question(request: QuestionGenerationRequest):
    """Generate an interview question using Ollama when available, otherwise use a template fallback."""
    fallback_question = question_generator.generate_question(request.topic, request.difficulty)

    if not ollama_client.available or not ollama_client.client:
        return QuestionGenerationResponse(
            question=fallback_question,
            source="template",
            model=request.model,
            fallback_used=True,
        )

    prompt = (
        f"Generate a single interview question about {request.topic} for a {request.difficulty} difficulty "
        "technical interview. Return only the question."
    )
    result = await ollama_client.generate_response(prompt, model=request.model or settings.ollama_default_model)
    generated_question = (result.get("response") or "").strip()

    if not generated_question or "error" in generated_question.lower():
        return QuestionGenerationResponse(
            question=fallback_question,
            source="template",
            model=request.model,
            fallback_used=True,
        )

    return QuestionGenerationResponse(
        question=generated_question,
        source="ollama",
        model=request.model or settings.ollama_default_model,
        fallback_used=False,
    )

@router.get("/ollama/health")
async def ollama_health():
    """Return the Ollama runtime health status."""
    return await ollama_client.health_check()

@router.get("/ollama/models")
async def ollama_models():
    """Return the list of available Ollama models."""
    return await ollama_client.list_models()
