# Architecture — WhatsApp RAG Chatbot

## Overview

A production-ready, RAG-grounded chatbot that answers user questions over
WhatsApp using company knowledge (documents, policies, FAQs, approved
historical chat) rather than general model knowledge or fine-tuning.

## Data Flow

```
User (WhatsApp)
  -> WhatsApp Cloud API -> Webhook (FastAPI)
  -> Conversation Manager (short-term memory: Redis, long-term memory: Postgres)
  -> Query Processor (language detection, coreference resolution using context)
  -> Retriever (hybrid: pgvector semantic search + Postgres keyword search)
  -> Reranker (optional, Phase 2)
  -> Context Assembly (top-k chunks + metadata + conversation history)
  -> LLM (Claude) - answers ONLY from assembled context
  -> Response Validator (grounding / confidence check)
  -> WhatsApp Cloud API -> User
```

## Why RAG over Fine-Tuning

Company knowledge (scholarship rules, prices, eligibility, deadlines) changes
frequently. RAG lets the knowledge base be updated by re-ingesting documents
with no model retraining. Fine-tuning is reserved for narrow, stable behaviors
(response style, intent classification) — never for facts that expire.

## Knowledge Priority Hierarchy

1. Current approved company policies
2. Current company documents
3. Verified structured knowledge (FAQs)
4. Approved human chat history (converted to structured Q&A during ingestion)
5. General model knowledge — only if explicitly enabled per deployment

If retrieval confidence falls below `RETRIEVAL_CONFIDENCE_THRESHOLD`, the bot
replies with a fallback ("I don't have enough verified information...")
instead of guessing.

## Memory

- **Short-term** (Redis, TTL-bound): last N turns of the active conversation,
  used purely for coreference resolution ("my CGPA is 3.4" -> later question).
- **Long-term** (Postgres `user_memory` table): a small set of structured
  fields only (education level, field of study, preferred country, intended
  degree). Free-text is never dumped into long-term memory. Deletable on
  user request via the admin API.

## Database

PostgreSQL (with the `pgvector` extension) holds both relational data
(users, conversations, messages, documents, escalations, feedback, audit
logs) and vector embeddings (`document_chunks.embedding`), avoiding a
second, separately-operated vector database for the MVP.

## WhatsApp Integration

Official WhatsApp Cloud API only. Webhook signature verification uses
`WHATSAPP_APP_SECRET` against Meta's `X-Hub-Signature-256` header — no
unofficial automation libraries.

## Security

- All secrets via environment variables, never committed (`.gitignore`
  excludes `.env`).
- Webhook signature verification on every inbound WhatsApp request.
- Rate limiting per phone number (Redis-backed).
- JWT auth for the admin panel.

## Phases

See `DEVELOPMENT.md` for the phase-by-phase build plan and current status.
