# RAG Project

This repository contains my Retrieval-Augmented Generation (RAG) project for the GenAI Secure Coding course. The project is built incrementally each week.

## Multi-Step Text Generation Flow

The `/generate-text` endpoint uses a **two-step pipeline** with Google Gemini (`gemini-2.5-flash`). Instead of asking the model to write a full story in one shot, the app breaks the task into planning and writing.

### Overview

```
Client request
    → Step 1: Generate a three-point outline
    → Step 2: Write the story using that outline
    → Return final story as JSON
```

### Step 1 — Outline

- **Prompt:** Ask Gemini to write a three-point outline for a short story about a cat.
- **Purpose:** Produce a lightweight structure (beginning, middle, end) before generating prose.
- **Output:** `step1_response.text` — the outline, passed into Step 2.

### Step 2 — Story

- **Prompt:** Ask Gemini to write the short story, including the outline from Step 1 in the prompt.
- **Purpose:** Turn the plan into a coherent narrative that follows the outline.
- **Output:** `step2_response.text` — returned to the client as `"text"` in the JSON response.

### Why the steps are separated

1. **Better structure** — Planning first tends to produce more organized stories than a single open-ended prompt.
2. **Clearer responsibilities** — Each call has one job (plan vs. write), which mirrors how multi-step LLM workflows are designed in production.
3. **Foundation for later work** — This pattern scales to RAG and agent flows where retrieval, reasoning, and generation happen in distinct stages.
4. **Easier debugging** — If the final story is weak, you can inspect whether the problem was the outline (Step 1) or the prose (Step 2).

### Error handling

Both steps run inside a single `try/except` block. If either Gemini call fails, the API returns HTTP 500 with a generic message and logs the error on the server.

## Running the app

```bash
cd rag-project
source venv_new/bin/activate
uvicorn rag_app:app --reload --host 127.0.0.1 --port 8000
```

Create a `.env` file with your API key (never commit this file):

```
GEMINI_API_KEY=your_key_here
```

### Test in the terminal

In a second terminal:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/generate-text
```

## Challenges and open questions

- **Syntax and structure** — Getting `try/except` indentation right and avoiding duplicate route definitions took care during development.
- **Latency and cost** — Two sequential API calls mean the endpoint takes longer (~10–20 seconds) and uses more tokens than a single-step prompt.
- **No outline in the response** — The API only returns the final story; exposing the Step 1 outline in the JSON could help with debugging and UI display.
- **Package deprecation** — `google.generativeai` shows a deprecation warning; migrating to `google.genai` may be needed later.
- **What’s next** — This week’s flow is multi-step prompting, not full RAG yet. Open questions include adding document retrieval, chunking, embeddings, and validating intermediate outputs before the next step runs.

## Git Commands Used So Far

- git clone
- git status
- git add
- git commit
- git push

## Project history

- Initial setup with basic project files
- Health endpoint and environment-based API key loading
- Multi-step `/generate-text` endpoint (outline → story)
