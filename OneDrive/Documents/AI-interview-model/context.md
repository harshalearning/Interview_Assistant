Here is a single self-contained context block you can reuse with any LLM to restart the project from scratch.

⸻

🧠 AI Mock Interview Assistant — Full Context (Reusable Prompt)

❓ Problem / Goal

I want to build a local AI-based mock interview assistant for programming and SDET (Software Development Engineer in Test) preparation.

The system should:

* Listen to spoken interview questions (from a friend or mock interviewer)
* Convert speech → text in real time
* Detect when a valid interview question is asked
* Generate a concise, structured answer
* Display the answer as text only (no voice output required)
* Help me practice answering questions in real-time interviews (mock practice only)

The system must:

* Work locally as much as possible
* Use free/open-source tools
* Minimize hallucinations (answers must be grounded in knowledge)
* Be modular and extensible
* Avoid treating my own speech as input to be re-answered
* Support SDET topics like:
    * Selenium, Playwright
    * API testing (REST Assured, Postman)
    * Java/Python
    * Automation frameworks
    * CI/CD
    * SQL
    * System design
    * Testing concepts and best practices

⸻

🎯 Expected Output Behavior

When a question is asked:

1. System listens to audio (microphone)
2. Converts speech → text (streaming)
3. Detects if it’s a valid question
4. If yes:
    * Retrieves relevant knowledge (if available)
    * Uses LLM to generate answer
    * Returns structured response like:

Definition:
Short explanation

Key Points:
- Point 1
- Point 2
- Point 3

Example:
Real-world or code example

Edge Cases:
Important caveats

Summary:
One-line recap


5. Display answer in a desktop overlay UI

⸻

🏗️ Proposed Architecture

We are NOT training an LLM from scratch.

We are building a system around an existing 8B parameter model.

Audio Input
   ↓
Speech-to-Text (Whisper / Faster-Whisper)
   ↓
Question Detection Layer
   ↓
Speaker Filtering (avoid self speech re-processing)
   ↓
RAG Retrieval (optional knowledge base)
   ↓
Local LLM (8B model via Ollama)
   ↓
Structured Answer Formatter
   ↓
UI Overlay (text output)

Model Strategy (Important)

We will use:

Local LLM (Free)

* Ollama runtime
* 8B models such as:
    * Llama 3 (8B)
    * Qwen 2.5 (7B/8B)
    * Mistral 7B
    * DeepSeek 7B

Why not train our own model?

Because:

* Training LLMs is expensive (GPU clusters, data, time)
* 8B models already perform well for reasoning
* We only need adaptation + orchestration, not training

⸻

📚 Knowledge Strategy (RAG)

We will improve accuracy using Retrieval Augmented Generation:

We store structured knowledge about:

* Programming languages
* Automation frameworks
* Testing concepts
* System design
* API testing
* DevOps tools

Question → Embedding → Vector DB → Relevant docs → LLM context → Answer

Tools:

* ChromaDB / FAISS
* Embeddings model (open-source or Ollama embedding support)

⸻

🎤 Speech System

We will use:

* Faster-Whisper (streaming speech-to-text)
* Microphone input
* Optional system audio capture (for mock interview partner)

We must handle:

Critical constraint:

The system must NOT re-process:

* Its own spoken/printed output
* Echo from speakers
* Self-generated answers

Solution:

* Speaker diarization OR
* Audio gating OR
* Simple rule: only process “interviewer channel” or mic priority filter

⸻

🧩 Core Features

1. Question Detection

Detect whether input is:

* Interview question → process
* Normal speech → ignore
* Self speech → ignore

⸻

2. Answer Generator

Use LLM with strict prompt:

* Concise
* Structured
* No hallucination preference
* Prefer grounded knowledge

⸻

3. RAG System (Optional but important)

Improves correctness by:

* Fetching relevant SDET + programming notes
* Injecting into prompt context

⸻

4. Memory Layer

Store:

* Last 10–20 questions
* Topic tracking
* Conversation flow

⸻

5. UI Layer

Simple desktop overlay:

* Always-on-top window
* Displays:
    * Question detected
    * Answer in structured format
* Optional shortcuts:
    * pause/resume listening
    * clear screen

⸻

🧪 Why we are building this

Purpose:

To create a personal AI mock interview trainer that helps:

* Practice SDET interviews
* Improve answering speed
* Learn structured communication
* Simulate real interview scenarios
* Get instant explanations of concepts

⸻

⚙️ Why this architecture

We are choosing this design because:

1. Cost efficiency

* Fully local system
* No API dependency

2. Control

* Custom prompts
* Custom knowledge base
* Adjustable behavior

3. Accuracy improvement

* RAG reduces hallucination
* Structured output improves clarity

4. Extensibility

We can later add:

* Coding question solving
* Interview scoring
* Voice reply mode
* Multi-language support
* Cloud sync (optional)

⸻

🚫 Constraints

* Do NOT build or depend on training a new LLM
* Must use existing 7B–8B open-source models
* Must prioritize local execution
* Must avoid reprocessing own speech
* Must minimize hallucination
* Must remain focused on learning / mock interview use case

⸻

🧱 High-level stack

* Python (core backend)
* Ollama (local LLM runtime)`
* Faster-Whisper (speech-to-text)
* ChromaDB / FAISS (vector DB)
* LangChain / LlamaIndex (or custom pipeline)
* FastAPI (API layer)
* PyQt / Electron (UI overlay)

⸻

🎯 Final outcome

A working system where:

I can speak a question during a mock interview → system listens → converts to text → detects question → retrieves knowledge → generates structured answer → displays it instantly on screen.

⸻

If you want next step, I can convert this into:

✔ GitHub-ready README
✔ Day-by-day implementation plan
✔ Folder structure + starter code
✔ First working prototype (Day 1 build)