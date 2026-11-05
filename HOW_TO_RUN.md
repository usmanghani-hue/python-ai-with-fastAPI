# Complete Workflow — Project Kaise Run Karein

Yeh file poora step-by-step workflow batati hai ke project ko local machine
par kaise setup aur run karna hai, shuru se le kar WhatsApp tak.

---

## 1. Zaroori Cheezen Install Karein (Prerequisites)

Yeh cheezen aapke computer par pehle se honi chahiye:

- **Docker Desktop** (Postgres + Redis + Backend sab isi se chalenge)
- **Git** (agar GitHub par push karna hai)
- Agar Docker use nahi karna to alag se:
  - **Python 3.12**
  - **PostgreSQL 16** (with `pgvector` extension)
  - **Redis**

Docker sab se aasan raasta hai — recommend yehi hai.

---

## 2. Project File Nikalna (Extract Karna)

```bash
unzip whatsapp-rag-bot-phase2.zip
cd whatsapp-rag-bot
```

---

## 3. Environment File Banana (.env)

Project mein secrets (API keys, passwords) `.env` file mein hote hain, jo
kabhi bhi GitHub par upload nahi hoti.

```bash
cp .env.example .env
```

Ab `.env` file ko kisi text editor mein khol kar yeh cheezen bharein:

| Variable | Kahan se milega |
|---|---|
| `ANTHROPIC_API_KEY` | console.anthropic.com se apni API key |
| `OPENAI_API_KEY` | platform.openai.com se apni API key (embeddings ke liye) |
| `WHATSAPP_PHONE_NUMBER_ID` | Meta Developer Console → WhatsApp → API Setup |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Meta Developer Console |
| `WHATSAPP_ACCESS_TOKEN` | Meta Developer Console (temporary ya permanent token) |
| `WHATSAPP_APP_SECRET` | Meta App Dashboard → Settings → Basic |
| `WHATSAPP_WEBHOOK_VERIFY_TOKEN` | Yeh aap khud koi bhi random string bana lein, e.g. `mySecret123` |
| `APP_SECRET_KEY` / `ADMIN_JWT_SECRET` | Koi bhi random lamba string bana lein |

**Abhi ke liye** (agar sirf project run karke dekhna hai, WhatsApp se connect
nahi karna) — sab jagah placeholder values rehne dein, backend phir bhi
start ho jayega. Sirf `/health` endpoint check karne ke liye real keys ki
zaroorat nahi.

---

## 4. Project Start Karna (Docker Se)

Project ke root folder (`whatsapp-rag-bot/`) mein ja kar:

```bash
docker compose up --build
```

Yeh command teen cheezen start karegi:
1. **Postgres** (database, port 5432)
2. **Redis** (memory/queue, port 6379)
3. **Backend** (FastAPI app, port 8000)

Terminal mein logs chalte rahenge — jab tak yeh command chal rahi hai,
project "on" hai. Band karne ke liye `Ctrl + C` dabayein, ya doosri terminal
mein:

```bash
docker compose down
```

---

## 5. Check Karna Ke Project Chal Raha Hai

Doosri terminal window khol kar:

```bash
curl http://localhost:8000/health
```

Response aisa milna chahiye:

```json
{"status": "ok", "env": "development"}
```

Agar yeh mil gaya, matlab backend successfully chal raha hai.

Browser mein bhi khol kar dekh sakte hain: `http://localhost:8000/health`

---

## 6. Roz Marra Ka Workflow (Development Ke Dauran)

Jab bhi code mein koi file change karein:

- Agar Docker volume mount hai (jo already `docker-compose.yml` mein set
  hai), to backend **automatically reload** ho jata hai — dobara start
  karne ki zaroorat nahi.
- Agar kabhi ajeeb error aaye ya changes nazar na aayen:
  ```bash
  docker compose down
  docker compose up --build
  ```

Naye packages (Python libraries) add karne ke baad hamesha rebuild karein
(`--build` flag) taake `requirements.txt` dobara install ho.

---

## 7. Without Docker (Agar Docker Use Nahi Karna)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows par: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Is soorat mein aapko khud se local Postgres (pgvector extension ke saath)
aur Redis install kar ke chalane honge, aur `.env` mein unke sahi
`DATABASE_URL` / `REDIS_URL` daalne honge.

---

## 8. Aam Ghaltiyan (Common Errors) Aur Hal

| Error | Wajah | Hal |
|---|---|---|
| `connection refused` port 5432/6379 par | Postgres/Redis abhi start nahi hua | Kuch second wait karein, phir `/health` check karein |
| `ModuleNotFoundError: No module named 'app'` | Ghalat folder se command chalayi | `whatsapp-rag-bot/` root folder se command chalayein, `app/` ke andar se nahi |
| `.env` field missing error | Koi zaroori variable `.env` mein nahi bhara | `.env.example` se compare kar ke missing field bharein |
| Port already in use | Koi doosra program port 8000/5432/6379 use kar raha hai | Woh program band karein, ya `docker-compose.yml` mein port number badal dein (e.g. `8001:8000`) |

---

## 9. Ab Tak Ka Status

Filhaal sirf **Phase 2 (Project Setup)** complete hai — matlab structure,
config, aur `/health` endpoint kaam kar rahe hain. Asal chatbot logic
(database, RAG, WhatsApp connection) abhi Phase 3 se aage banega. Jab
woh phases ban jayenge, yeh workflow file update ho kar unke run/test
steps bhi shamil karegi (e.g. webhook test karna, database migrate karna,
sample sawal poochna).
