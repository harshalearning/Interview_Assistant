# mock-interview-ai

A modular scaffold for a mock interview AI system.

## Project Structure

- `backend/` - API endpoints and orchestration logic
- `speech/` - speech capture, playback, and voice processing
- `llm/` - model adapters, prompt engineering, and LLM calls
- `rag/` - retrieval-augmented generation pipelines
- `ui/` - user interface or desktop client components
- `memory/` - session and conversation memory management
- `data/` - datasets, vector stores, and assets
- `docs/` - design docs, architecture notes, and references
- `tests/` - automated tests and validation
- `main.py` - FastAPI application entrypoint
- `requirements.txt` - Python dependencies

## Setup

1. Install Python 3.11+.
2. Install Git and VS Code.
3. Install Ollama and FFmpeg.
4. Create a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
5. Install project dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
6. Copy the example environment file and configure Ollama settings if needed:
   ```powershell
   copy .env.example .env
   notepad .env
   ```
7. Start the backend server:
   ```powershell
   uvicorn main:app --reload
   ```

## Development Notes

- Use `git` feature branches for new work.
- Commit early and keep changes small.
- Place reusable backend logic in `backend/` and keep data assets in `data/`.
- Keep UI-specific code in `ui/` and speech/audio code in `speech/`.

## Ollama Basics

- Verify installation with `ollama version`.
- Use `ollama list` to see available models.
- Use models with the Python client or CLI as needed.
- Configure runtime settings in `.env` using `.env.example`.
- The app exposes Ollama status endpoints at:
  - `GET /api/v1/ollama/health`
  - `GET /api/v1/ollama/models`

## FFmpeg

- Verify FFmpeg is installed with `ffmpeg -version`.
- FFmpeg is useful for audio format conversion and recording support.

## Verify

- Run unit tests with:
  ```powershell
  pytest
  ```
- Confirm the API is running at `http://127.0.0.1:8000/`.
