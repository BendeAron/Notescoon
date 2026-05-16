# Deployment (Render + Neon)

Target architecture: **single-origin** (FastAPI serves the built React app).

## 1) Neon (Postgres)

- Create a Neon project + database.
- Copy the connection string.
- Use it as `DATABASE_URL` on Render.

Tip: if Neon gives you `postgresql://...` this backend will auto-normalize it to the `postgresql+psycopg://...` driver.

## 2) Render (Docker web service)

This repo includes a multi-stage [Dockerfile](Dockerfile) that:
- builds the React app (Vite → `dist/`)
- runs FastAPI and serves `dist/` with SPA fallback

Create a new **Web Service** on Render:
- Runtime: Docker
- Health check path: `/health`

### Env vars

- `ENV=production`
- `SECRET_KEY` = long random string
- `DATABASE_URL` = Neon connection string (include `sslmode=require` if Neon requires it)

### Migrations (production)

After first deploy (or whenever migrations change), run:

```bash
cd backend
alembic upgrade head
```

How you run that depends on Render (shell / one-off job). Keep it to one instance at a time.

## 3) Verify

- `GET /` serves the React app.
- `GET /health` returns `{"status":"ok"}`.
- Register/login + notes CRUD works end-to-end.
