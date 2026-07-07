"""Tests for backend API."""

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "version" in response.json()


def test_ping():
    """Test ping endpoint."""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_session():
    """Test session creation."""
    response = client.post("/api/v1/sessions/create", params={
        "user_id": "user123",
        "topic": "Python"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "user123"
    assert data["topic"] == "Python"
    assert data["status"] == "active"


def test_get_session():
    """Test session retrieval."""
    # Create session first
    create_response = client.post("/api/v1/sessions/create", params={
        "user_id": "user123",
        "topic": "Python"
    })
    session_id = create_response.json()["id"]
    
    # Get session
    response = client.get(f"/api/v1/sessions/{session_id}")
    assert response.status_code == 200
    assert response.json()["id"] == session_id


def test_add_question_to_session():
    """Test adding question to session."""
    # Create session
    create_response = client.post("/api/v1/sessions/create", params={
        "user_id": "user123",
        "topic": "Python"
    })
    session_id = create_response.json()["id"]
    
    # Add question
    question_data = {
        "question": "What is Python?",
        "topic": "Python",
        "difficulty": "easy"
    }
    response = client.post(
        f"/api/v1/sessions/{session_id}/questions/add",
        json=question_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "added"


def test_update_session_status():
    """Test updating session status."""
    # Create session
    create_response = client.post("/api/v1/sessions/create", params={
        "user_id": "user123",
        "topic": "Python"
    })
    session_id = create_response.json()["id"]
    
    # Update status
    response = client.patch(
        f"/api/v1/sessions/{session_id}/status",
        params={"status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["new_status"] == "completed"


def test_generate_question_endpoint():
    """Test the LLM question generation endpoint."""
    response = client.post(
        "/api/v1/llm/generate-question",
        json={"topic": "Python", "difficulty": "easy"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "question" in data
    assert data["question"]
    assert data["source"] in {"ollama", "template"}


def test_ollama_health_endpoint():
    """Test the Ollama health endpoint."""
    response = client.get("/api/v1/ollama/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_ollama_models_endpoint():
    """Test the Ollama models endpoint."""
    response = client.get("/api/v1/ollama/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
