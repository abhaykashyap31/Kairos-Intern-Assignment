# Scientific‑Paper Scout

A model-agnostic AI agent that helps users discover and summarize recent research papers from arXiv, with support for multiple LLM providers (OpenAI, Anthropic, Gemini) and both CLI and web-based interfaces.

---

## Features

- **Search arXiv** for recent papers on any topic.
- **Summarize scientific PDFs** using your choice of LLM provider.
- **Model-agnostic:** Switch LLMs (OpenAI, Anthropic, Gemini) via config/env, no code changes needed.
- **CLI chat interface** (required) and **optional web UIs** (React, Streamlit).
- **Tool call logging:** Every tool call (name, args, timestamps, outcome, latency) is logged and shown to the user.
- **Extensible:** Easily add new MCP servers or LLM providers.

---

## Architecture Overview

```
User (CLI/React/Streamlit)
   |
   v
[Agent Host (Python)]
   |         | \
   |         |  \
   v         v   v
[paper_search] [pdf_summarize] [...]
```

### Components

| Component                | Tech/Location         | Description                                                                                                    |
|--------------------------|----------------------|----------------------------------------------------------------------------------------------------------------|
| **Agent Host**           | `agent_host/agent.py`| Receives user messages, routes to MCP servers, streams responses, logs tool calls. Model-agnostic.             |
| **paper_search MCP**     | `mcp_servers/paper_search.py` | Queries arXiv API for papers matching a query. Returns metadata.                                 |
| **pdf_summarize MCP**    | `mcp_servers/pdf_summarize.py`| Downloads PDF, extracts text, summarizes using configured LLM. Supports OpenAI, Anthropic, Gemini.             |
| **CLI Chat**             | `main.py`            | Command-line chat interface. Streams responses, prints tool call logs.                                         |
| **API Server (optional)**| `api_server.py`      | FastAPI backend for web UIs. POST `/api/chat` endpoint.                                                        |
| **React Frontend (opt.)**| `react-frontend/`    | Modern web UI (Vite + React + TS). Connects to API server.                                                     |
| **Streamlit UI (opt.)**  | `streamlit_app.py`   | Simple web UI for chat and paper search/summarization.                                                         |
| **Config**               | `config.py`, `config.yaml` | Loads LLM provider/model from config or env. Model-agnostic.                                         |

---

## Setup & Installation

1. **Clone the repo and enter the directory:**
   ```sh
   git clone <repo-url>
   cd kairos-take-home\ Intern\ Assignment
   ```
2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **(Optional) Install frontend dependencies:**
   ```sh
   cd react-frontend && npm install
   ```

---

## Configuration

The system is **model-agnostic**: you can switch LLM providers and models via config, no code changes needed.

- **Via environment variables** (recommended for quick changes):
  ```
  LLM_PROVIDER=openai   # or anthropic, gemini
  LLM_MODEL=gpt-3.5-turbo  # or claude-3-sonnet-20240229, gemini-2.0-pro, etc
  ```
- **Or via `config.yaml`:**
  ```yaml
  LLM_PROVIDER: openai
  LLM_MODEL: gpt-3.5-turbo
  ```
- **API keys:** Set the appropriate environment variables for your provider:
  - `OPENAI_API_KEY` for OpenAI
  - `ANTHROPIC_API_KEY` for Anthropic
  - `GOOGLE_API_KEY` for Gemini

---

## Usage

### 1. CLI Chat (Required)

Run the CLI interface:
```sh
python main.py
```

**Commands:**
- `search <topic>` — Find recent papers on a topic (uses arXiv)
- `summarize <pdf_url>` — Summarize a scientific paper from a PDF URL (arXiv or direct link)
- `quit` or `exit` — Exit the chat

**Example:**
```
You: search graph neural networks
[Tool call] paper_search | Args: {'query': 'graph neural networks', 'max_results': 5} | ...
Assistant:
Title: ...
Authors: ...
Summary: ...
Link: ...
---

You: summarize https://arxiv.org/abs/2106.04554
[Tool call] pdf_summarize | Args: {'pdf_url': 'https://arxiv.org/pdf/2106.04554.pdf'} | ...
Assistant:
<detailed summary>
```

### 2. API Server (Optional, for Web UIs)

Start the FastAPI server:
```sh
uvicorn api_server:app --reload
```
- **Endpoint:** `POST /api/chat` with `{ "message": "..." }`
- **Response:** `{ "response": "...", "tool_calls": [ ... ] }`

### 3. React Frontend (Optional)

1. Start the backend API (see above).
2. In `react-frontend/`:
   ```sh
   npm run dev
   ```
3. Open [http://localhost:5173](http://localhost:5173)

- Modern chat UI, shows LLM config, supports search/summarize commands.
- Communicates with backend via `/api/chat`.

### 4. Streamlit UI (Optional)

```sh
streamlit run streamlit_app.py
```
- Simple web UI for chat, search, and summarization.
- Shows LLM provider/model in sidebar.

---

## How It Works

### Agent Host (`agent_host/agent.py`)
- Receives user messages (from CLI, API, or UI).
- Routes to the correct MCP server based on keywords (`search`, `summarize`).
- Logs every tool call (name, args, timestamps, outcome, latency) to both console and logger.
- Streams responses line-by-line to the user.
- Uses LLM provider/model from config/env (model-agnostic).

### MCP Servers
- **paper_search:**
  - Queries arXiv API for papers matching the user's query.
  - Returns a list of papers (title, authors, summary, link).
- **pdf_summarize:**
  - Downloads the PDF (auto-converts arXiv abs links to PDF links).
  - Extracts text using PyPDF2.
  - Summarizes the first ~4000 characters using the configured LLM provider (OpenAI, Anthropic, Gemini).
  - Uses a technical prompt to preserve detail and terminology.
  - Returns `{ "summary": "..." }`.

### Model-Agnostic LLM Integration
- LLM provider/model are loaded at runtime from config/env.
- Supported providers: OpenAI, Anthropic, Gemini (Google).
- Each provider uses its official SDK and API key.
- Easy to add new providers by extending `call_llm` in `pdf_summarize.py`.

### Logging
- Every tool call is logged with name, args, timestamps, outcome, and latency.
- Logs are printed to the console and available in API responses.

---

## Dependencies

All dependencies are listed in `requirements.txt`. Key packages:
- `requests`, `PyPDF2` — Core functionality
- `openai`, `anthropic`, `google-generativeai` — LLM providers
- `fastapi`, `uvicorn`, `pydantic` — API server
- `streamlit` — Optional UI
- `PyYAML`, `python-dotenv` — Config loading
- `react`, `vite`, `styled-components`, `axios` — (in `react-frontend/`)

---

## Extending the System

- **Add new MCP servers:** Create a new module in `mcp_servers/` and add routing logic in `AgentHost`.
- **Add new LLM providers:** Extend `call_llm` in `pdf_summarize.py`.
- **Change UI:** Use the API server for custom web/mobile clients.

---

## Troubleshooting

- Make sure you have the correct API keys set for your chosen LLM provider.
- If you see import errors for LLM SDKs, install the missing package (see `requirements.txt`).
- For PDF summarization, ensure the PDF is accessible and not encrypted.

---

## License

MIT (or specify your license here)


