# Development Roadmap

Build is incremental — each phase only depends on files that already exist.

| Phase | Name | Status |
|---|---|---|
| 1 | Architecture & tech decisions | Done |
| 2 | Project setup | Done |
| 3 | Backend (API routes, service layer) | Done |
| 4 | Database (models, pgvector setup) | Done (using `create_all`, not yet Alembic) |
| 5 | Knowledge ingestion pipeline | Done — see `TRAINING_GUIDE.md` |
| 6 | RAG (retrieval + generation) | Done — hybrid search, no reranker yet |
| 7 | Conversation memory (short + long term) | Done |
| 8 | WhatsApp Cloud API integration | Code done — see `WHATSAPP_META_SETUP_GUIDE.md` for your own account setup |
| 9 | Admin dashboard | API-only (no visual dashboard yet) — see `TRAINING_GUIDE.md` |
| 10 | Testing & evaluation dataset | Basic unit tests only (`tests/test_ingestion_utils.py`) |
| 11 | Security hardening | Basic (webhook signature verify, admin key, env-based secrets) — needs review before real production use |
| 12 | Deployment (dev/staging/prod) | Pending |
| 13 | Monitoring / observability | Basic structlog logging only |
| 14 | Production optimization | Pending |

## What's Actually Working Right Now

- `POST /chat/test` — talk to the bot without WhatsApp (great for
  testing ingestion results)
- `POST /admin/documents/ingest-text` — add knowledge (documents, FAQs,
  chat history)
- `GET /admin/documents` / `DELETE /admin/documents/{id}` — manage
  knowledge
- `GET /webhook` + `POST /webhook` — WhatsApp webhook (needs your Meta
  credentials in `.env` and a public URL — see
  `WHATSAPP_META_SETUP_GUIDE.md`)
- Short-term memory (Redis) + long-term structured memory (Postgres)
- Hybrid retrieval (pgvector semantic + Postgres keyword search)
- Confidence-based fallback when no relevant knowledge is found

## What's Still Missing (Be Aware)

- **Visual admin dashboard** — right now knowledge management is via
  API (Swagger UI at `/docs`), not a clickable web page. A real Next.js
  dashboard is a separate build.
- **Alembic migrations** — schema changes currently require dropping
  and recreating tables; fine for development, not for production data.
- **Reranking, PDF/DOCX file upload, human handoff, full observability
  dashboards, deployment automation** — all still pending.

## Local Setup (Phase 2)

1. Copy environment file:
   ```bash
   cp .env.example .env
   ```
   Fill in real values: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, WhatsApp
   credentials (from Meta Developer Console), and generate random strings
   for `APP_SECRET_KEY` / `ADMIN_JWT_SECRET`.

2. Start Postgres + Redis + backend:
   ```bash
   docker compose up --build
   ```

3. Confirm it's running:
   ```bash
   curl http://localhost:8000/health
   # {"status": "ok", "env": "development"}
   ```

4. Without Docker (local Python):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8000
   ```
   (Requires Postgres with the `pgvector` extension and Redis running
   locally, matching the URLs in `.env`.)

## Common Errors (Phase 2)

- **`pydantic_settings.exceptions.SettingsError` / missing field** — a
  required variable in `.env` is missing. Check it against
  `.env.example`; every non-defaulted field in `app/config.py` must be set.
- **`connection refused` on port 5432/6379** — Postgres or Redis containers
  aren't up yet; `docker compose up` and wait a few seconds before hitting
  `/health`.
- **`ModuleNotFoundError: No module named 'app'`** — run uvicorn from the
  project root (`whatsapp-rag-bot/`), not from inside `app/`.

## Next Phase

**Phase 3 — Backend**: build out `app/api/whatsapp.py`, `app/api/chat.py`,
`app/api/admin.py` route stubs and `app/services/` service classes
(`llm_service.py`, `rag_service.py`, `memory_service.py`,
`whatsapp_service.py`, `ingestion_service.py`) with clear interfaces, before
wiring in the database in Phase 4.
