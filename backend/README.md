# Notescoon backend

## Local dev (Windows / macOS / Linux)

### 1) Start Postgres

From the repo root:

```bash
docker compose up -d
```

### 2) Configure env vars

Copy the example file and adjust as needed:

```bash
cd backend
copy .env.example .env
```

### 3) Create a virtualenv + install deps

```bash
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
```

### 4) Run the API

```bash
python -m uvicorn app.main:app --reload --port 8000
```

Health check:
- http://localhost:8000/health
