# Architecture Overview

This project is organized around a modular AI interview application.

## Components

- `backend/`
  - API endpoints
  - orchestration and application services

- `speech/`
  - audio capture and playback
  - speech-to-text and text-to-speech integration

- `llm/`
  - model wrappers and prompt management
  - Ollama and other LLM backend adapters

- `rag/`
  - data retrieval and vector search
  - context injection for better answer generation

- `ui/`
  - desktop or web user interface logic
  - presenter and input/output components

- `memory/`
  - conversation state tracking
  - long-term memory and session persistence

- `data/`
  - raw content, embeddings, and metadata
  - vector store persistence and indexing assets

## Workflow

1. Capture user intent from `ui/` or `speech/`.
2. Convert audio to text in `speech/`.
3. Use `llm/` and `rag/` to generate answers.
4. Store and retrieve state from `memory/`.
5. Serve results through `backend/`.
