# Workflow — Cloud Database + Local Python (Docker Ke Bagair)

Is workflow mein Docker bilkul install nahi karna. Sirf Python apne
computer par chalega, aur Database + Redis free cloud services se milenge.

---

## Step 1 — Postgres (with pgvector) Banayein — Neon Se

1. [neon.tech](https://neon.tech) par jaayein aur free account banayein
   (GitHub/Google se sign up ho jata hai).
2. **"Create a project"** par click karein.
3. Project ban jane ke baad, dashboard par **"Connection String"** milegi,
   kuch aisi:
   ```
   postgresql://username:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. pgvector extension enable karne ke liye, Neon ke **SQL Editor** mein
   yeh query chalayein:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
   (Neon mein pgvector already support hota hai, bas extension "on" karna
   padta hai — ek dafa ka kaam hai.)

> Alternative: [supabase.com](https://supabase.com) bhi same tarah kaam
> karta hai, aur wahan bhi pgvector Database → Extensions se enable hota
> hai.

---

## Step 2 — Redis Banayein — Upstash Se

1. [upstash.com](https://upstash.com) par free account banayein.
2. **"Create Database"** par click karein, region select karein.
3. Dashboard par **"Redis Connect"** section mein connection URL milegi,
   kuch aisi:
   ```
   redis://default:password@xxxxx.upstash.io:6379
   ```

---

## Step 3 — `.env` File Update Karein

Apni `.env` file khol kar yeh do lines replace karein:

```env
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxxxx.us-east-2.aws.neon.tech/neondb
REDIS_URL=redis://default:password@xxxxx.upstash.io:6379
```

**Zaroori:** Neon ki connection string mein `postgresql://` hota hai, lekin
hamare app mein `asyncpg` driver use ho raha hai, isliye shuru mein
`postgresql+asyncpg://` likhna hai (upar wale example mein yehi kiya gaya
hai). `?sslmode=require` wala part hata dein — asyncpg ke liye alag se
`ssl=true` chahiye hota hai; abhi ke liye ise chorr dein, Phase 4
(Database) mein hum connection setup mein SSL properly handle karenge.

Baaki saari `.env` values (ANTHROPIC_API_KEY, OPENAI_API_KEY, waghera)
pehle jaisi hi rehne dein.

---

## Step 4 — Python Environment Banayein

Project ke root folder (`whatsapp-rag-bot/`) mein:

```bash
python -m venv .venv
```

Activate karein:

- **Mac/Linux:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  .venv\Scripts\activate
  ```

Activate hone ke baad terminal ke shuru mein `(.venv)` nazar aayega.

---

## Step 5 — Dependencies Install Karein

```bash
pip install -r requirements.txt
```

Yeh sab zaroori Python libraries (FastAPI, SQLAlchemy, Anthropic SDK,
waghera) install kar dega.

---

## Step 6 — Backend Start Karein

```bash
uvicorn app.main:app --reload --port 8000
```

Terminal mein aisa kuch dikhega:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 7 — Check Karein Ke Chal Raha Hai

Doosri terminal window mein:

```bash
curl http://localhost:8000/health
```

Response:

```json
{"status": "ok", "env": "development"}
```

Ya browser mein khol lein: `http://localhost:8000/health`

---

## Roz Marra Ka Workflow

- Code change karne par `--reload` flag ki wajah se server khud restart ho
  jata hai — kuch alag se karne ki zaroorat nahi.
- Jab bhi naya terminal session khulay, dobara `.venv` activate karna na
  bhoolein (Step 4), warna `ModuleNotFoundError` aayega.
- Kaam khatam karne ke baad terminal mein `Ctrl + C` se server band karein.

---

## Common Errors

| Error | Wajah | Hal |
|---|---|---|
| `password authentication failed` | Neon/Upstash ki connection string mein galti | Dashboard se dobara connection string copy karein |
| `SSL connection required` | Neon ko SSL chahiye hota hai | Abhi ke liye ignore karein — Phase 4 mein SSL config properly add hoga |
| `ModuleNotFoundError: No module named 'app'` | Ghalat folder se command chalayi | `whatsapp-rag-bot/` root se command chalayein |
| `command not found: uvicorn` | `.venv` activate nahi hai | Step 4 dobara karein |

---

## Status

Yeh setup Phase 2 (project skeleton) ke liye kaafi hai. Phase 4 (Database)
mein hum SQLAlchemy models aur Alembic migrations banayenge jo isi Neon
database par tables bana denge — connection string abhi se ready hai,
kuch aur karne ki zaroorat nahi.
