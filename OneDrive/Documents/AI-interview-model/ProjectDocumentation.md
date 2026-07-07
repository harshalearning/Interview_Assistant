# mock-interview-ai Project Documentation

**Date Created:** July 3, 2026  
**Project Location:** `c:\Users\harsh\OneDrive\Documents\AI-interview-model`

---

## Overview

This document captures the complete setup and initialization of the **mock-interview-ai** project, a modular AI-powered interview simulation system. The project is designed with a clean architecture supporting speech processing, LLM integration, retrieval-augmented generation (RAG), and a responsive user interface.

---

## 1. Project Structure

### Folder Hierarchy

```
mock-interview-ai/
│
├── backend/              # API endpoints and orchestration logic
├── speech/               # Audio capture, playback, and voice processing
├── llm/                  # Model adapters, prompt engineering, LLM calls
├── rag/                  # Retrieval-augmented generation pipelines
├── ui/                   # User interface or desktop client components
├── memory/               # Session and conversation memory management
├── data/                 # Datasets, vector stores, and assets
├── docs/                 # Design docs, architecture notes, and references
├── tests/                # Automated tests and validation
├── main.py               # FastAPI application entrypoint
├── requirements.txt      # Python dependencies
├── README.md             # Project setup and basic usage guide
├── .gitignore            # Git ignore patterns for Python and VS Code
└── ProjectDocumentation.md  # This file
```

### Package Initialization

All module folders include `__init__.py` stubs to enable Python package imports:

- `backend/__init__.py` - Backend package marker
- `speech/__init__.py` - Speech package marker
- `llm/__init__.py` - LLM package marker
- `rag/__init__.py` - RAG package marker
- `ui/__init__.py` - UI package marker
- `memory/__init__.py` - Memory package marker
- `data/__init__.py` - Data package marker
- `tests/__init__.py` - Test package marker

---

## 2. Files Created

### Core Application Files

#### `main.py`
FastAPI application entrypoint with basic routing:
- `GET /` - Health check endpoint returning status and available endpoints
- `GET /ping` - Simple ping/pong test endpoint

**Status:** Ready for extension with business logic

#### `requirements.txt`
Comprehensive Python dependency list:
- **Web Framework:** fastapi, uvicorn
- **Speech Processing:** faster-whisper
- **Vector Database:** chromadb
- **Embeddings:** sentence-transformers
- **LLM Integration:** langchain, ollama
- **UI:** pyqt6
- **Audio:** sounddevice, numpy
- **Deep Learning:** torch
- **Testing:** pytest
- **Utilities:** requests

**Total Packages:** 13 direct dependencies (70+ including transitive deps)

#### `README.md`
Quick-start guide containing:
- Project structure overview
- Setup instructions (Python, venv, package installation)
- Ollama basics and FFmpeg setup
- Git workflow recommendations
- Verification and testing instructions

#### `.gitignore`
Excludes non-essential files from version control:
- Virtual environment (`.venv/`)
- Python bytecode (`__pycache__/`, `.pyc`, `.pyo`)
- Log files (`.log`)
- Database files (`.sqlite3`, `.db`)
- Editor config (`.vscode/`, `.env`)
- OS artifacts (`.DS_Store`)

### Documentation Files

#### `docs/architecture.md`
Component architecture document describing:
- **backend/** - API endpoints and orchestration
- **speech/** - Audio I/O and voice processing
- **llm/** - Model wrappers and prompt management
- **rag/** - Vector retrieval and context injection
- **ui/** - User interface logic
- **memory/** - State and conversation storage
- **data/** - Assets and vector store persistence

Includes workflow diagram showing data flow through components.

### Test Files

#### `tests/test_main.py`
Pytest test suite with 2 passing tests:
- `test_read_root()` - Validates health check endpoint
- `test_ping()` - Validates ping endpoint

Uses FastAPI's `TestClient` for endpoint testing.

---

## 3. Python Environment Setup

### Virtual Environment Creation

**Command:** `python -m venv .venv`

**Location:** `.venv/` folder in project root

**Status:** ✓ Successfully created and configured

### Python Version

- **Detected:** Python 3.13.5
- **Required:** Python 3.11+
- **Status:** ✓ Compatible

### Dependency Installation

**Command:** `.venv\Scripts\python.exe -m pip install -r requirements.txt`

**Process:**
1. pip upgraded from 25.1.1 to 26.1.2
2. All packages resolved with metadata inspection
3. Large downloads (torch: 123.0 MB, PyQt6-Qt6: 78.4 MB, etc.)
4. Compilation of C/C++ extensions (ctranslate2, onnxruntime, scipy)
5. Total installation time: ~2-3 minutes

**Installation Statistics:**
- Total packages installed: 70+
- Successfully installed: 100%
- Failed: 0
- Warnings: 1 (related to FastAPI's TestClient deprecation—non-blocking)

### Verification

**Command:** `.venv\Scripts\python.exe -c "import fastapi; import ollama; import torch; print('✓ All core packages imported successfully')"`

**Result:** ✓ All critical packages (FastAPI, Ollama, PyTorch) imported successfully

---

## 4. Testing & Validation

### Test Execution

**Command:** `.venv\Scripts\python.exe -m pytest tests/ -v`

**Results:**
```
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
collected 2 items

tests/test_main.py::test_read_root PASSED                    [ 50%]
tests/test_main.py::test_ping PASSED                         [100%]

============================== 2 passed in 0.54s ==========================
```

**Status:** ✓ All tests passing

---

## 5. Development Workflow

### Running the Application

To start the development server:

```powershell
cd "c:\Users\harsh\OneDrive\Documents\AI-interview-model"
.\.venv\Scripts\Activate.ps1
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Interactive Documentation:**
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Code Organization Principles

1. **Modular Design:** Each component in its own folder with clear responsibilities
2. **Separation of Concerns:** Backend logic, speech processing, LLM, UI are isolated
3. **Shared Utilities:** Use `backend/` for shared services
4. **Data Management:** Store assets and vector stores in `data/`
5. **Testing:** Unit tests colocated with functionality in `tests/`

### Git Integration

Initialize repository (not yet done):
```powershell
git init
git add .
git commit -m "Initial project scaffold with base architecture"
git branch -M main
```

---

## 6. Architecture Overview

### Component Interaction Workflow

```
User Input (UI/Speech)
    ↓
speech/ → Convert to text or receive input
    ↓
backend/ → Route to appropriate handler
    ↓
llm/ + rag/ → Generate contextual responses
    ↓
memory/ → Store conversation state
    ↓
speech/ → Convert to audio or return output
    ↓
UI → Display results
```

### Key Design Decisions

1. **FastAPI:** Async-ready, automatic API documentation, type safety
2. **Ollama:** Offline LLM support, no external API dependencies
3. **ChromaDB:** Lightweight vector database for RAG without external services
4. **PyTorch:** Foundation for custom NLP models if needed
5. **Faster-Whisper:** Efficient speech-to-text with offline capability

---

## 7. Next Steps & Future Work

### Immediate (Phase 1)
- [ ] Initialize Git repository and create initial commit
- [ ] Set up CI/CD pipeline (GitHub Actions or similar)
- [ ] Create API models and schemas in `backend/`
- [ ] Build basic speech capture/playback in `speech/`

### Short-term (Phase 2)
- [ ] Implement LLM wrapper for Ollama in `llm/`
- [ ] Set up vector store indexing in `rag/`
- [ ] Build PyQt6 UI shell in `ui/`
- [ ] Create conversation memory service in `memory/`

### Medium-term (Phase 3)
- [ ] Integrate speech-to-text pipeline
- [ ] Build interview question generation engine
- [ ] Implement feedback generation
- [ ] Add user profile and analytics

### Long-term (Phase 4)
- [ ] Multi-language support
- [ ] Advanced voice cloning
- [ ] Real-time voice feedback
- [ ] Mobile app support

---

## 8. Troubleshooting

### Virtual Environment Issues

**Issue:** `Access is denied` when removing `.venv`
- **Solution:** Use `Remove-Item -Recurse -Force` instead of `rmdir /s /q` in PowerShell

**Issue:** `Activate.ps1` not recognized
- **Solution:** This is a PowerShell execution policy issue; not a blocker for pip installation

### Installation Issues

**Issue:** Large downloads timeout
- **Solution:** Increase pip timeout: `pip install --default-timeout=1000 -r requirements.txt`

**Issue:** CUDA-related errors with torch
- **Solution:** CPU-only torch is installed; GPU support requires separate CUDA/cuDNN setup

---

## 9. Development Environment

### System Information
- **OS:** Windows (PowerShell 5.1+)
- **Python:** 3.13.5
- **Workspace Location:** `C:\Users\harsh\OneDrive\Documents\AI-interview-model`
- **Editor:** VS Code (recommended)

### Recommended VS Code Extensions
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- FastAPI (tiangolo.fastapi-vscode)
- Pytest (littlefoxteam.vscode-python-test-adapter)

### Environment Management
- **Package Manager:** pip 26.1.2
- **Test Runner:** pytest 9.1.1
- **Virtual Environment Manager:** venv (stdlib)

---

## 10. Dependency Summary

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| fastapi | 0.139.0 | Web framework |
| uvicorn | 0.49.0 | ASGI server |
| faster-whisper | 1.2.1 | Speech-to-text |
| chromadb | 1.5.9 | Vector database |
| sentence-transformers | 5.6.0 | Embeddings |
| langchain | 1.3.11 | LLM orchestration |
| ollama | 0.6.2 | Ollama Python client |
| pyqt6 | 6.11.0 | Desktop UI |
| sounddevice | 0.5.5 | Audio I/O |
| torch | 2.12.1 | Deep learning |
| numpy | 2.5.0 | Numerical computing |
| pytest | 9.1.1 | Testing framework |
| requests | 2.34.2 | HTTP client |

### Transitive Dependencies
- **starlette** 1.3.1 - ASGI toolkit (FastAPI dependency)
- **pydantic** 2.13.4 - Data validation (FastAPI dependency)
- **transformers** 5.12.1 - Hugging Face models (LLM dependency)
- **scikit-learn** 1.9.0 - Machine learning utilities
- **scipy** 1.18.0 - Scientific computing
- **grpcio** 1.81.1 - gRPC for distributed services

---

## 11. Project Status

### Completed ✓
- [x] Project scaffold created
- [x] Folder structure established
- [x] All core files generated
- [x] Python virtual environment set up
- [x] Dependencies installed
- [x] Tests passing
- [x] Documentation completed

### In Progress
- [ ] Git repository initialization
- [ ] Backend API development
- [ ] Speech module implementation

### Pending
- [ ] UI development
- [ ] LLM integration testing
- [ ] RAG pipeline setup
- [ ] End-to-end testing

---

## 12. Quick Reference Commands

### Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### Run Tests
```powershell
.venv\Scripts\python.exe -m pytest tests/ -v
```

### Start Development Server
```powershell
uvicorn main:app --reload
```

### Install New Packages
```powershell
.venv\Scripts\python.exe -m pip install <package-name>
```

### View Installed Packages
```powershell
.venv\Scripts\python.exe -m pip list
```

### Generate Requirements Snapshot
```powershell
.venv\Scripts\python.exe -m pip freeze > requirements-freeze.txt
```

---

**Document Version:** 1.0  
**Last Updated:** July 3, 2026  
**Maintained By:** Development Team
