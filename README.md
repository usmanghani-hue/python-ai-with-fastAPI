# WhatsApp RAG Chatbot

Production-ready, RAG-grounded, human-like chatbot that answers user
questions over WhatsApp using approved company knowledge (documents,
policies, FAQs, and structured historical chat) — not free-floating model
knowledge, and not fine-tuning.

See:
- `ARCHITECTURE.md` — full system design, data flow, and design rationale
- `DEVELOPMENT.md` — phase-by-phase build plan, current status, local setup

## Quick Start

```bash
cp .env.example .env      # fill in real API keys and WhatsApp credentials
docker compose up --build
curl http://localhost:8000/health
```

## Stack

FastAPI · PostgreSQL + pgvector · Redis · Anthropic Claude · OpenAI
embeddings · WhatsApp Cloud API (official)

## Status

Phase 2 of 14 complete (project setup). See `DEVELOPMENT.md` for the full
roadmap and what's next.
