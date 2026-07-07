# Getting Started - mock-interview-ai

**Quick Integration Guide**

---

## 0. Configure Environment

Copy `.env.example` to `.env` and update the Ollama settings if needed:

```powershell
copy .env.example .env
notepad .env
```

---

## 1. Start the API Server

Open a terminal in the project directory:

```powershell
cd "c:\Users\harsh\OneDrive\Documents\AI-interview-model"
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

---

## 2. Access API Documentation

Open your browser and navigate to:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

You can test all endpoints interactively in the Swagger UI.

---

## 3. API Usage Examples

### Create a New Interview Session

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sessions/create?user_id=user123&topic=Python"
```

**Response:**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "user123",
  "topic": "Python",
  "status": "active",
  "questions": [],
  "responses": [],
  "created_at": "2026-07-03T10:30:00.000000",
  "updated_at": "2026-07-03T10:30:00.000000"
}
```

### Add a Question to Session

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sessions/{session_id}/questions/add" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?",
    "topic": "Python",
    "difficulty": "easy"
  }'
```

### Submit an Answer

**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/sessions/{session_id}/responses/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "q1",
    "response_text": "Python is a high-level programming language..."
  }'
```

### Get Session Status

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/sessions/{session_id}"
```

### Update Session Status

**Request:**
```bash
curl -X PATCH "http://127.0.0.1:8000/api/v1/sessions/{session_id}/status?status=completed"
```

### Check Ollama Health

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/ollama/health"
```

### List Ollama Models

**Request:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/ollama/models"
```

---

## 4. Using Core Modules in Your Code

### Speech Processing

```python
from speech.processor import AudioProcessor, SpeechToText

# Record audio
processor = AudioProcessor()
audio = processor.capture_audio(duration=5)  # Record for 5 seconds

# Transcribe audio
stt = SpeechToText(model="base")
result = await stt.transcribe("audio.wav")
print(result["text"])
```

### LLM Integration

```python
from llm.models import InterviewQuestionGenerator, OllamaClient

# Generate questions
generator = InterviewQuestionGenerator()
question = generator.generate_question("Python", difficulty="medium")

# Get LLM response (with Ollama)
client = OllamaClient()
response = await client.generate_response(
    prompt="What is OOP?",
    model="llama2"
)
```

### Memory Management

```python
from memory.session import SessionManager, UserProfile

# Create session manager
manager = SessionManager()
session = manager.create_session("sess1", "user1", "Python")

# Track conversation
session.conversation.add_message("user", "Hello")
session.conversation.add_message("assistant", "Hi! How can I help?")

# Update metrics
session.increment_metric("questions_asked", 1)
session.update_metric("total_score", 8.5)

# Get session info
print(session.to_dict())
```

### RAG and Knowledge Base

```python
from rag.retrieval import KnowledgeBase

# Initialize knowledge base
kb = KnowledgeBase()

# Index knowledge
await kb.index_knowledge(
    topic="Python",
    content="Python is a high-level, interpreted programming language...",
    metadata={"source": "Wikipedia"}
)

# Retrieve context for a question
context = await kb.retrieve_context("What is Python?", topic="Python")
print(context)
```

### Data Management

```python
from data.manager import DatasetManager, CacheManager

# Create and manage datasets
dataset_mgr = DatasetManager()
dataset = dataset_mgr.create_dataset(
    "Python Basics",
    "Basic Python interview questions",
    "python"
)

# Add questions
dataset_mgr.add_question_to_dataset(
    dataset["id"],
    "What is a list?",
    "A list is an ordered collection...",
    "easy"
)

# Use cache
cache = CacheManager(ttl=3600)
cache.set("key1", "value1")
value = cache.get("key1")
```

---

## 5. Running Tests

### Run All Tests
```powershell
.venv\Scripts\python.exe -m pytest tests/ -v
```

### Run Specific Test File
```powershell
.venv\Scripts\python.exe -m pytest tests/test_api.py -v
```

### Run with Coverage
```powershell
pip install pytest-cov
.venv\Scripts\python.exe -m pytest --cov=. tests/
```

**Current Status:** 27/27 tests passing ✓

---

## 6. Module Overview

| Module | Purpose | Key Files |
|--------|---------|-----------|
| **backend** | API endpoints & sessions | api.py |
| **speech** | Audio I/O & transcription | processor.py |
| **llm** | Ollama & prompt management | models.py |
| **rag** | Vector DB & retrieval | retrieval.py |
| **memory** | Sessions & conversations | session.py |
| **data** | Data persistence | manager.py |
| **ui** | UI components | components.py |

---

## 7. Configuration & Customization

### Audio Settings
```python
processor = AudioProcessor(sample_rate=44100)
```

### LLM Models
```python
# Different Whisper models
stt = SpeechToText(model="large")

# Different Ollama models
client = OllamaClient()
response = await client.generate_response(
    prompt="...",
    model="mistral",  # or any Ollama model
    temperature=0.5,
    max_tokens=512
)
```

### Vector Store
```python
# Custom embedding model
from rag.retrieval import EmbeddingGenerator
embeddings = EmbeddingGenerator(model_name="all-mpnet-base-v2")
```

### UI Themes
```python
from ui.components import ThemeManager
light_theme = ThemeManager.get_theme("light")
dark_theme = ThemeManager.get_theme("dark")
```

---

## 8. Troubleshooting

### API Won't Start
- Check if port 8000 is available
- Verify virtual environment is activated
- Run: `pip install -r requirements.txt`

### Import Errors
- Ensure you're using the venv Python: `.venv\Scripts\python.exe`
- Check working directory is project root

### Tests Failing
- Make sure venv is activated
- Run `pip install -r requirements.txt`
- Check file permissions

### Audio Issues
- Verify sounddevice is installed
- Check microphone is connected and enabled
- Test with `sounddevice.list_devices()`

---

## 9. Next Steps

1. **Configure Ollama** - Install and run Ollama locally
2. **Set up Vector DB** - Initialize ChromaDB with sample data
3. **Build UI** - Create PyQt6 interface
4. **Add Database** - Replace in-memory storage with PostgreSQL/SQLite
5. **Deploy** - Set up Docker container and cloud deployment

---

## 10. Useful Commands

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run API server
uvicorn main:app --reload

# Run tests
pytest tests/ -v

# Check dependencies
pip list

# Install new package
pip install <package-name>

# Export requirements
pip freeze > requirements.txt

# View API docs
start http://127.0.0.1:8000/docs
```

---

## 11. Project Structure

```
mock-interview-ai/
├── main.py              # FastAPI entry point
├── requirements.txt     # Dependencies
├── backend/api.py       # API endpoints
├── speech/processor.py  # Audio & speech
├── llm/models.py        # LLM integration
├── rag/retrieval.py     # Vector DB
├── memory/session.py    # Memory management
├── data/manager.py      # Data storage
├── ui/components.py     # UI widgets
├── tests/               # Test suite
└── docs/                # Documentation
```

---

## Support & Resources

- **API Documentation:** http://127.0.0.1:8000/docs
- **Project Docs:** See `ProjectDocumentation.md`
- **Status Report:** See `STATUS_REPORT.md`
- **Architecture:** See `docs/architecture.md`

---

**Ready to build!** 🚀

For questions or issues, refer to the documentation files in the project.
