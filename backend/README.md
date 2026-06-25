# Company Intelligence Backend (Localhost Setup)

This backend runs fully on your local machine:
- FastAPI for API
- Ollama for local LLM inference
- Offline HTML files from `backend/data/offline_sites`

## What LLM client is used?

The project uses **Ollama HTTP API client** in `app/llm/llm_client.py`.

Current default model (optimized for lower-end PCs):
- `qwen2.5:1.5b`

You can change it in `app/config.py` using:
- `LLM_MODEL`
- `LLM_BASE_URL`
- `LLM_NUM_CTX`
- `LLM_TIMEOUT`

## Quick start

1) Install Python packages
```bash
pip install -r requirements.txt
```

2) Start Ollama and pull the default lightweight model
```bash
ollama pull qwen2.5:1.5b
ollama serve
```

3) Run backend on localhost
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

4) Test in browser
- [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Endpoints

- `GET /api/lookup?domain=example.com`
- `GET /api/graph/{domain}`
- `GET /api/companies`

## Data folders

- Input HTML: `backend/data/offline_sites/<domain>/`
- Output cache: `backend/data/processed/<domain>.json`

## Performance tip for mid-range PCs

If responses feel slow, keep these defaults:
- model: `qwen2.5:1.5b`
- context: `2048`
- timeout: `180`
