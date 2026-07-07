# Project Notes

## Current status
- FastAPI backend is running with session management endpoints.
- Ollama configuration is wired through environment settings.
- New endpoint `/api/v1/llm/generate-question` is available and falls back to template-based questions if Ollama is unavailable.
- Health and model listing endpoints are exposed at `/api/v1/ollama/health` and `/api/v1/ollama/models`.

## Next steps
- Pull a real Ollama model such as `llama3.2` and validate the generation endpoint end to end.
- Connect generated questions to the interview session workflow.
- Add answer evaluation and session persistence.
