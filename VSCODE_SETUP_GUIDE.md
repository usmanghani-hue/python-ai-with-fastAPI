# VS Code Mein Project Setup Aur Run Karne Ka Poora Guide

Yeh guide bilkul shuru se hai. Maan kar chal rahe hain VS Code pehle se
install nahi hai.

---

## Step 1 — VS Code Install Karein

1. [code.visualstudio.com](https://code.visualstudio.com) par jaayein.
2. Bara neela button **"Download for Windows"** dabayein.
3. Downloaded installer (`VSCodeUserSetup...exe`) ko double-click karein.
4. License agreement accept karein → **"Next"** → **"Next"** karte jaayein.
5. Ek screen par **"Additional Tasks"** milegi — yeh sab checkbox tick kar
   dein, khaas kar:
   - "Add to PATH"
   - "Register Code as an editor for supported file types"
6. **"Install"** dabayein, phir **"Finish"**.

---

## Step 2 — VS Code Mein Python Extension Install Karein

1. VS Code khulne ke baad, left side bar mein **Extensions** icon par
   click karein (chaar chotay squares wala icon), ya `Ctrl + Shift + X`
   dabayein.
2. Search box mein likhein: `Python`
2. Microsoft ka official **"Python"** extension dhoondh kar **"Install"**
   dabayein.

---

## Step 3 — Project Folder Ko VS Code Mein Kholein

1. VS Code mein upar **File** menu → **"Open Folder..."**
2. Apni project folder select karein:
   ```
   Downloads\whatsapp-rag-bot-phase2\whatsapp-rag-bot
   ```
3. **"Select Folder"** dabayein.

Ab left side mein saari project files (`app`, `requirements.txt`, `.env`,
`README.md` waghera) ek list mein nazar aayengi.

---

## Step 4 — VS Code Ka Built-in Terminal Kholein

Alag se Command Prompt kholne ki zaroorat nahi — VS Code ke andar hi
terminal hota hai:

1. Upar menu se **Terminal** → **"New Terminal"**
   (ya shortcut: `` Ctrl + ` `` — yani Ctrl aur backtick key)
2. Neeche ek terminal panel khul jayega, jismein aap seedha commands
   likh sakte hain — yeh bilkul waisa hi hai jaisa Command Prompt.

---

## Step 5 — Sahi Python Version Select Karein (3.12)

Agar aap ne pehle Python 3.12 install kar liya hai (pandas error fix ke
liye), to VS Code ko batana hoga ke wahi version use kare:

1. `Ctrl + Shift + P` dabayein (Command Palette khulegi).
2. Type karein: `Python: Select Interpreter`
3. List mein se **Python 3.12.x** wala option select karein.

Agar list mein 3.12 nazar na aaye, to VS Code terminal mein yeh command
se manually venv create kar lein (agar pehle se nahi bani):
```
py -3.12 -m venv .venv
```
Phir dobara `Ctrl + Shift + P` → `Python: Select Interpreter` → is baar
`.venv` wala option dikhega, usay select kar lein.

---

## Step 6 — Virtual Environment Activate Karein

VS Code terminal mein:

```
.venv\Scripts\activate
```

Agar Step 5 mein interpreter already `.venv` set kar diya tha, to naya
terminal kholte hi yeh **automatically activate** ho jata hai — terminal
line ke shuru mein `(.venv)` likha nazar aayega.

---

## Step 7 — Libraries Install Karein

```
pip install -r requirements.txt
```

Yeh 1-3 minute legi. Complete hone ka wait karein.

---

## Step 8 — `.env` File Check Karein

Left side files list mein `.env` par click karein — VS Code mein hi khul
jayegi editing ke liye. Confirm karein:
- `DATABASE_URL` mein Neon wali sahi connection string hai (`+asyncpg`
  ke saath, `?sslmode=require` ke bagair)
- Baaki placeholder values (`APP_SECRET_KEY` waghera) khaali nahi hain

---

## Step 9 — Server Run Karein

Terminal mein:

```
uvicorn app.main:app --reload --port 8000
```

Yeh dikhna chahiye:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

---

## Step 10 — Browser Mein Test Karein

Browser mein yeh address kholein:
```
http://localhost:8000/health
```

Yeh milna chahiye:
```json
{"status": "ok", "env": "development"}
```

---

## Roz Marra Ka Workflow (Ab Se Aage)

Jab bhi kaam karna ho:
1. VS Code kholein → project folder already khula rahega (last opened
   folder yaad rakhta hai)
2. Naya terminal kholein (`` Ctrl + ` ``) — `.venv` khud activate ho
   jayega
3. `uvicorn app.main:app --reload --port 8000` chalayein
4. Kaam khatam hone par terminal mein `Ctrl + C` dabayein server band
   karne ke liye

Code mein koi bhi file change karenge, to `--reload` flag ki wajah se
server khud restart ho jayega — dobara command chalane ki zaroorat nahi.

---

## Common Errors

| Error | Hal |
|---|---|
| Terminal mein `(.venv)` nazar nahi aa raha | Step 5-6 dobara karein |
| `uvicorn is not recognized` | `.venv` activate nahi hai, ya `pip install` complete nahi hui |
| VS Code neeche "Select Interpreter" ka prompt de | Us par click kar ke 3.12 wala `.venv` select kar lein |

---

## Agla Kadam

VS Code setup ho gaya, server chal raha hai. Ab agla kaam hai:

1. **Phase 3 — Backend**: API routes aur service files banana
2. **Phase 4 — Database**: Neon par tables banana
3. **Phase 5 — Knowledge Ingestion**: chat history/documents ko
   "train" karne wala pipeline (yani data ko process kar ke database
   mein store karna)
4. **Phase 8 — WhatsApp**: Meta Developer Console setup + webhook code

Yeh sab phases banne ke baad hi WhatsApp integration aur chat-history
training ka real, working guide di ja sakti hai — kyunke tab tak woh
code exist hi nahi karta jise guide follow kar ke chalaya ja sake.
