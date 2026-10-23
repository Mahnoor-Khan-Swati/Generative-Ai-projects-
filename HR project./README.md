# HR Multi-Agent Assistant

An enterprise-style **multi-agent HR assistant** built on LangChain's composable
`Runnable` primitives (`RunnablePassthrough`, `RunnableLambda`, `RunnableBranch`,
`RunnableParallel`, `RunnableSequence`), served through a FastAPI backend with a
built-in chat UI.

An employee asks a question in plain language ("How many leave days do I have
left?"), the pipeline classifies the intent, routes it to one of six specialized
HR agents, runs eight retrieval/validation tasks concurrently, and returns a
merged, cited, personalized answer — escalating to a human HR rep when the data
can't fully resolve the request.

## Architecture

```
Employee Query
      │
      ▼
RunnablePassthrough        preserves the raw query
      │
      ▼
RunnableLambda              clean text, detect language, extract employee ID,
(preprocessing)             attach employee metadata
      │
      ▼
RunnableBranch               classify intent → route to one of:
(routing)                    Leave · Payroll · Benefits · Recruitment ·
                              IT Support · General HR
      │
      ▼
RunnableParallel              8 concurrent tasks:
                               retrieve_policies · search_employee_records ·
                               query_database · rag_retrieval ·
                               generate_llm_response · check_permissions ·
                               summarize_documents · check_escalation
      │
      ▼
RunnableLambda                merge results, validate, format citations,
(post-processing)             decide on human escalation
      │
      ▼
Final Personalized HR Response
```

This exact flow lives in `app/chains/pipeline.py`, wired together with the
`|` operator into one `RunnableSequence`.

## Project structure

```
hr-multi-agent-assistant/
├── app/
│   ├── main.py                 FastAPI app: /api/chat, /api/health, static UI
│   ├── config.py                env vars + mock "database" loaders
│   ├── models.py                Pydantic request/response schemas
│   ├── chains/
│   │   ├── preprocessing.py     RunnablePassthrough + RunnableLambda
│   │   ├── routing.py           RunnableBranch intent classification
│   │   ├── parallel_tasks.py    RunnableParallel (8 concurrent tasks)
│   │   ├── postprocessing.py    RunnableLambda merge & format
│   │   ├── pipeline.py          RunnableSequence — wires it all together
│   │   └── llm.py               ChatGoogleGenerativeAI (Gemini) wrapper, falls back to MockLLM
│   ├── agents/                  one class per specialized HR agent
│   ├── data/                    mock JSON "databases" (employees, leave,
│   │                             payroll, HR policy knowledge base)
│   └── static/                  chat UI (HTML/CSS/JS, no build step)
├── tests/
│   └── test_pipeline.py         end-to-end pipeline tests
├── requirements.txt
├── .env.example
├── run.sh / run.bat             one-command launchers
└── README.md
```

## Requirements

- Python 3.10+
- No API key required to run the demo — it falls back to a deterministic
  mock LLM. Set `GOOGLE_API_KEY` in `.env` to use a real Gemini model instead.
  Get a free key at https://aistudio.google.com/app/apikey

## Quick start

### 1. Open the project in VS Code

```bash
cd hr-multi-agent-assistant
code .
```

### 2. Run it — one command

macOS / Linux:

```bash
chmod +x run.sh
./run.sh
```

Windows (VS Code integrated terminal, cmd or PowerShell):

```bat
run.bat
```

The script creates a virtual environment, installs dependencies, copies
`.env.example` to `.env` on first run, and starts the server at
**http://127.0.0.1:8000**.

### 3. Or run it manually, step by step

```bash
# 1. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env             # Windows: copy .env.example .env
# (optional) add your GOOGLE_API_KEY inside .env

# 4. Run the server
uvicorn app.main:app --reload
```

Open **http://127.0.0.1:8000** in your browser — the chat UI is served
directly from the FastAPI app.

## Trying it out

The mock data includes three employees: `E1001`, `E1002`, `E1003`. Type an
ID into the sidebar (or mention it in your question, e.g. "What's my leave
balance, I'm E1001?") and ask things like:

- "How many leave days do I have left?"
- "When will my salary be credited?"
- "How do I enroll in health insurance?"
- "Are there any internal job openings?"
- "I forgot my VPN password."

Ask something outside these categories and it falls back to the **General
HR Agent** and flags the request for human escalation.

## Running tests

```bash
pytest -v
```

## API

| Method | Path          | Description                              |
|--------|---------------|-------------------------------------------|
| GET    | `/`           | Chat UI                                   |
| GET    | `/api/health` | Pipeline status + which LLM mode is active |
| POST   | `/api/chat`   | `{ "query": str, "employee_id": str\|null }` → full pipeline response |

## Extending this project

- **Real databases**: swap the JSON loaders in `app/config.py` for calls to
  your HRIS / payroll system.
- **Real intent classification**: replace the keyword scorer in
  `app/chains/routing.py` with an LLM-based classifier — the `RunnableBranch`
  wiring around it doesn't need to change.
- **Real document retrieval**: swap `_rag_retrieval` in
  `app/chains/parallel_tasks.py` for a vector store retriever
  (e.g. Chroma, FAISS, pgvector).
- **Auth**: `check_permissions` is a stub — wire it to your actual identity



ya brower ma run kar dy
http://127.0.0.1:8000/