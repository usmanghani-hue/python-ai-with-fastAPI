# Resume Prompt

You are continuing work on the existing WhatsApp RAG Bot project.

Project path on Windows:
`D:\whatsapp-rag-bot\whatsapp-rag-bot`

Important context:
- This is a Python FastAPI backend.
- Run it without Docker.
- The project uses Neon PostgreSQL with pgvector and Redis.
- Configuration is in `.env`; never print or expose secret values.
- Database connection is loaded from `DATABASE_URL` in `.env`.
- Neon URLs may contain `sslmode=require`; the project converts this for asyncpg in `app/database/connection.py`.
- Do not replace, reset, or delete the existing Neon database.
- Existing database data and chat history must be preserved.
- Chat history source file is `whatsapp-export-combined.txt`.
- Chat history is ingested as RAG knowledge; it is not model fine-tuning.
- Existing start and stop scripts are `start.ps1` and `stop.ps1`.
- Existing tests must continue to pass.

When continuing this project:
1. Change to the project directory.
2. Inspect the relevant files before editing.
3. Do not use Docker unless explicitly requested.
4. Do not expose `.env` values, API keys, passwords, or tokens.
5. Start the backend with `./start.ps1` when a running server is needed.
6. Stop it with `./stop.ps1` when finished or before switching projects.
7. Check the backend with `curl.exe http://localhost:8000/health`.
8. Use the existing `.venv` Python environment.
9. Before changing database code, verify the current Neon connection and preserve existing data.
10. After edits, run focused validation and `python -m pytest -q` when appropriate.
11. Make minimal changes and report exactly what was changed and tested.

Useful commands:

```powershell
cd D:\whatsapp-rag-bot\whatsapp-rag-bot
.\.venv\Scripts\Activate.ps1
.\start.ps1
curl.exe http://localhost:8000/health
```

To stop the project:

```powershell
cd D:\whatsapp-rag-bot\whatsapp-rag-bot
.\stop.ps1
```

Continue from the user's latest request, not from scratch. First inspect the current repository state and then take the smallest safe action needed.
