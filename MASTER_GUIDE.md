# MASTER GUIDE — Poora Roadmap, Shuru Se Aakhir Tak

Yeh ek hi file hai jo sab kuch order mein batati hai. Bas isi ko follow
karte jaayein, upar se neeche.

**Kaunsi zip use karni hai:** `whatsapp-rag-bot-full.zip`
(`whatsapp-rag-bot-phase2.zip` ab use nahi karni — woh purani, khaali
skeleton thi.)

---

# HISSA 1 — VS Code Mein Setup Aur Run Karna (Abhi Karna Hai)

## 1.1 — Zip Extract Karein

1. `whatsapp-rag-bot-full.zip` ko **Downloads** folder mein rakhein.
2. Us par right-click → **"Extract All"** → **"Extract"**.
3. `whatsapp-rag-bot` naam ki folder khul jayegi — yehi project hai.

## 1.2 — VS Code Install Karein (Agar Pehle Se Nahi Hai)

[code.visualstudio.com](https://code.visualstudio.com) se download karein,
install karein, "Add to PATH" wala checkbox tick rakhein.

## 1.3 — Python 3.12 Install Karein (Agar Pehle Se Nahi Hai)

[python.org/downloads/release/python-31210](https://www.python.org/downloads/release/python-31210/)
se download karein. Install karte waqt **"Add python.exe to PATH"**
checkbox zaroor tick karein.

(Agar aap ne pichle steps mein yeh already kar liya hai, to skip kar
dein.)

## 1.4 — Project Ko VS Code Mein Kholein

1. VS Code kholein.
2. **File → Open Folder** → `whatsapp-rag-bot` folder select karein.
3. Left side mein saari files (`app`, `requirements.txt`, waghera)
   dikhengi.

## 1.5 — Terminal Kholein Aur Virtual Environment Banayein

VS Code mein `` Ctrl + ` `` dabayein terminal kholne ke liye. Phir:

```
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Confirm karein `(.venv)` terminal ke shuru mein likha hai.

## 1.6 — Libraries Install Karein

```
pip install -r requirements.txt
```

1-3 minute lagega. Complete hone ka wait karein.

## 1.7 — `.env` File Banayein

1. Project folder mein `.env.example` file ko copy karein, naam
   `.env` rakhein (detail steps `WINDOWS_ENV_SETUP_GUIDE.md` mein hain
   agar yeh confusing lage).
2. Isme yeh cheezen bharni hain — **abhi ke liye sirf pehli 3 cheezen
   zaroori hain taake server chal sake**, baaki baad mein:

   | Variable | Abhi Zaroori? | Kahan Se Milega |
   |---|---|---|
   | `DATABASE_URL` | **Haan** | Neon.tech se (pehle bana chuke hain) |
   | `REDIS_URL` | **Haan** | Upstash.com se free Redis banayein |
   | `APP_SECRET_KEY`, `ADMIN_JWT_SECRET` | **Haan** | Khud koi random text likh dein, jaise `mySecret123` |
   | `ANTHROPIC_API_KEY` | Server chalane ke liye zaroori hai (khaali nahi ho sakta) | console.anthropic.com |
   | `OPENAI_API_KEY` | Server chalane ke liye zaroori hai | platform.openai.com |
   | `WHATSAPP_*` saari values | **Abhi nahi** | Baad mein — Hissa 3 dekhein |

   **Zaroori:** `ANTHROPIC_API_KEY` aur `OPENAI_API_KEY` ke bina server
   crash ho jayega (config file inhe required maangti hai). Agar abhi
   real keys nahi hain, to bhi in fields mein koi bhi text daal dein
   (jaise `sk-ant-placeholder`) taake server start ho jaye — jis din
   asal training (Hissa 2) karni ho, us din real keys chahiye hongi.

3. `DATABASE_URL` mein Neon wali string daalte waqt yaad rahe:
   - `postgresql://` ko `postgresql+asyncpg://` banana hai
   - Aakhir se `?sslmode=require` hatana hai

## 1.8 — Redis Banayein (Upstash Se)

1. [upstash.com](https://upstash.com) par free account banayein.
2. **"Create Database"** → koi bhi region select karein.
3. Dashboard par milne wali **Redis connection URL** copy karein
   (`redis://default:password@....upstash.io:6379` jaisi).
4. `.env` mein `REDIS_URL` ke against paste kar dein.

## 1.9 — Server Run Karein

```
uvicorn app.main:app --reload --port 8000
```

Yeh dikhna chahiye:
```
INFO:     Application startup complete.
```

Agar yeh line aa gayi — matlab database se connection ban gaya, tables
khud ban gaye (pgvector extension ke sath), aur server chal raha hai.

## 1.10 — Browser Mein Confirm Karein

```
http://localhost:8000/health
```
Yeh milna chahiye: `{"status": "ok", "env": "development"}`

**Bas — Hissa 1 complete.** Backend chal raha hai, database connected
hai. Yahan tak koi WhatsApp ya training ki zaroorat nahi thi.

---

# HISSA 2 — Data Se Train Karna (Jab Sir Data De Dein)

Jab aapke paas company ka data (FAQs, policies, purani chat history)
aa jaye, tab yeh karna hai:

1. Browser mein kholein: `http://localhost:8000/docs`
2. Yahan se data ko system mein daalna hai — **poora tarika**
   `TRAINING_GUIDE.md` file mein detail se likha hai.
3. Short mein: `POST /admin/documents/ingest-text` endpoint use hota
   hai, jahan aap title + text + category daal kar submit karte hain —
   system khud usay clean, chunk, aur searchable bana deta hai.

Jab yeh step aaye, `TRAINING_GUIDE.md` follow karein — wahan
step-by-step, example ke saath likha hai.

---

# HISSA 3 — WhatsApp Se Connect Karna (Sab Se Aakhir Mein)

Jab data train ho jaye aur bot `/docs` ke through sahi jawab dene lage,
tab WhatsApp connect karna hai. Iske liye:

1. `WHATSAPP_META_SETUP_GUIDE.md` file follow karein.
2. Yeh Meta Developer account banane, tokens lene, aur webhook connect
   karne ka poora guide hai — yeh sirf aap khud kar sakte hain (apne
   Facebook/Meta account se).

---

# Abhi Kya Karna Hai (Summary)

Aap abhi **Hissa 1** par hain. Bas yeh order follow karein:
1. Zip extract karein
2. VS Code + Python 3.12 install karein (agar nahi hai)
3. `.env` banayein, Neon + Upstash connect karein
4. `pip install -r requirements.txt`
5. `uvicorn app.main:app --reload --port 8000`
6. `http://localhost:8000/health` check karein

Jahan bhi atkein, us step ka screenshot bhej dein — main saath dekh kar
batata hoon.
