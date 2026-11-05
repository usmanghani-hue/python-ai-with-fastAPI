# Complete Beginner Guide — Shuru Se Aakhir Tak

Yeh guide bilkul shuru se hai. Har step follow karein, koi bhi step skip
na karein.

---

## Step 1 — Text Editor Install Karein (VS Code)

`.env` file ko edit karne ke liye ek simple text editor chahiye.
Recommend: **VS Code** (free hai).

1. [code.visualstudio.com](https://code.visualstudio.com) par jaayein
2. **Download** button dabayein (apne system ke mutabiq — Windows/Mac)
3. Download hone ke baad install kar lein (normal software install jaisa
   hi hai — "Next, Next, Finish")

---

## Step 2 — Project Folder Dhoondein / Nikalein

Pehle jo `whatsapp-rag-bot-phase2.zip` file maine di thi, woh aapke
computer par **Downloads** folder mein honi chahiye.

1. **Downloads** folder kholein
2. `whatsapp-rag-bot-phase2.zip` par **right-click** karein
3. **"Extract All"** (Windows) ya double-click (Mac) se usay extract karein
4. Ab aapko ek folder milega naam **`whatsapp-rag-bot`**

Is folder ko kisi aasan jagah move kar lein, jaise Desktop par, taake
dobara dhoondna na pare. Misal ke tor par: `Desktop/whatsapp-rag-bot`

---

## Step 3 — Project Folder Ko VS Code Mein Kholein

1. VS Code app kholein
2. Upar left corner mein **File** menu par click karein
3. **"Open Folder..."** par click karein
4. Woh `whatsapp-rag-bot` folder select karein (jo Step 2 mein nikala tha)
5. **Select Folder** / **Open** dabayein

Ab left side mein aapko project ki saari files ki list nazar aa jayegi —
`app`, `tests`, `README.md`, `.env.example`, waghera.

---

## Step 4 — `.env` File Banayein

Zaroori baat: `.env` naam ki file abhi project mein maujood **nahi** hai.
Sirf `.env.example` hai — jo ek "template" hai. Hamein iski copy bana kar
naam se `.` hata kar `.env` rakhna hai.

### Tareeqa (VS Code Ke Andar):

1. Left side file list mein **`.env.example`** par right-click karein
2. **"Copy"** par click karein
3. Khaali jagah (list mein) par right-click karein, **"Paste"** karein
4. Nayi file ka naam `.env.example copy` ya kuch aisa hoga — usay
   **rename** karein (right-click → Rename) aur naam rakhein bilkul:
   ```
   .env
   ```
   (Sirf yeh 4 characters: dot, e, n, v — kuch aur nahi)

Ab aapke paas do files honi chahiye: `.env.example` (asli template, ise mat
chhairein) aur `.env` (yeh wali edit karni hai).

---

## Step 5 — `.env` File Kholein Aur Values Bharein

1. Left list mein **`.env`** par click karein — yeh khul jayegi
2. Ismein bohat sari lines hongi jaisay:
   ```
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```
3. Har line ke `=` ke baad wali value ko apni asli value se replace karna
   hai. Neeche step-by-step likha hai kahan se kya milega.

### 5.1 — DATABASE_URL (Neon Se)

Neon dashboard mein wapis jaayein:
1. **"Show password"** par click karein (stars hat jayenge)
2. **"Copy snippet"** par click karein — poori string copy ho jayegi

Ab `.env` file mein `DATABASE_URL=` wali puri line delete kar ke yeh
 likhein (apni copy ki hui string paste karein, lekin do cheezen badalni
hain):

**Neon se jo milega (misal):**
```
postgresql://neondb_owner:ABCD1234@ep-broad-morning-axdjhpke.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require
```

**`.env` mein yeh likhna hai** (do farq: `postgresql+asyncpg://` aur
aakhir mein `?sslmode=require` hata dena):
```
DATABASE_URL=postgresql+asyncpg://neondb_owner:ABCD1234@ep-broad-morning-axdjhpke.c-4.us-east-2.aws.neon.tech/neondb
```

⚠️ Yahan `ABCD1234` sirf misal hai — aapko apna asli password wahan
paste karna hai jo Neon se copy hua.

### 5.2 — REDIS_URL (Upstash Se — Abhi Banana Hai)

Agar Upstash account nahi banaya abhi tak:
1. [upstash.com](https://upstash.com) par jaayein
2. **Sign up** karein (Google/GitHub se ho jata hai, free hai)
3. **"Create Database"** dabayein
4. Koi naam de dein (misal: `whatsapp-bot`), region select karein (jo
   aapke qareeb ho), **Create** dabayein
5. Database ban jane ke baad, dashboard par **"Redis Connect"** ya
   **"REST API"** section mein `redis://...` se shuru hone wali string
   milegi
6. Woh copy karein aur `.env` mein `REDIS_URL=` ke aage paste kar dein

### 5.3 — Baaki Cheezen (Abhi Ke Liye Placeholder Rehne Dein)

In cheezon ki abhi zaroorat nahi (agla phase WhatsApp integrate karte
waqt inko bharenge). Filhaal `.env.example` mein jo likha hai wahi rehne
dein:
```
WHATSAPP_PHONE_NUMBER_ID=xxxxxxxxxxxxxxx
WHATSAPP_BUSINESS_ACCOUNT_ID=xxxxxxxxxxxxxxx
WHATSAPP_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxx
WHATSAPP_APP_SECRET=xxxxxxxxxxxxxxxxxxxxx
```

**Yeh do zaroor bharni hain** (LLM aur embeddings ke liye — bagair inke
chatbot kaam nahi karega, lekin abhi sirf server start karne ke liye bhi
zaroori nahi, sirf placeholder rehne dein filhaal):
```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
```
(Anthropic key console.anthropic.com se, OpenAI key platform.openai.com
se milti hai — jab chatbot ka asal jawab dena wala part banayenge tab
zaroori hongi.)

**Yeh do koi bhi random text bana kar daal dein** (kam se kam 20
characters, kuch bhi random likh dein):
```
APP_SECRET_KEY=yehKoiBhiRandomLambaStringHaiXYZ123
ADMIN_JWT_SECRET=yehBhiKoiRandomStringHaiABC456
```

4. File save karein: **Ctrl + S** (Windows) ya **Cmd + S** (Mac)

---

## Step 6 — Terminal Kholein

VS Code ke andar hi terminal khul sakta hai:

1. Upar menu mein **Terminal** par click karein
2. **"New Terminal"** par click karein
3. Neeche ek black/dark window khul jayegi — yehi terminal hai

(Yeh terminal already `whatsapp-rag-bot` folder ke andar hoga, kyunke
humne yehi folder VS Code mein khola tha.)

---

## Step 7 — Python Environment Banayein

Terminal mein yeh command likh kar **Enter** dabayein:

```bash
python -m venv .venv
```

Agar error aaye `python: command not found`, to `python3` try karein:
```bash
python3 -m venv .venv
```

Kuch second lagega, phir wapis normal line aa jayegi (matlab ho gaya).

---

## Step 8 — Environment Activate Karein

**Mac ya Linux ho to:**
```bash
source .venv/bin/activate
```

**Windows ho to:**
```bash
.venv\Scripts\activate
```

Agar sahi se hua to terminal ke bilkul shuru mein `(.venv)` likha nazar
aayega, kuch aisa:
```
(.venv) yourname@computer whatsapp-rag-bot %
```

---

## Step 9 — Dependencies Install Karein

Terminal mein (jab `(.venv)` nazar aa raha ho):

```bash
pip install -r requirements.txt
```

Yeh thora time lega (1-3 minute), bohat sari lines print hongi — yeh
normal hai, wait karein jab tak khatam na ho.

---

## Step 10 — Server Start Karein

```bash
uvicorn app.main:app --reload --port 8000
```

Yeh dikhna chahiye:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Agar yeh dikh gaya — **mubarak ho, server chal raha hai!**

---

## Step 11 — Check Karein Ke Kaam Kar Raha Hai

Browser kholein aur yeh address likhein:
```
http://localhost:8000/health
```

Yeh dikhna chahiye:
```json
{"status":"ok","env":"development"}
```

Yeh mil gaya to sab sahi hai.

---

## Agli Baar Jab Kaam Karna Ho

Har naya session shuru karte waqt:
1. VS Code kholein, `whatsapp-rag-bot` folder open karein
2. Terminal kholein
3. Environment activate karein (Step 8 wali command)
4. Server start karein (Step 10 wali command)

`.env` file dobara banane ki zaroorat nahi — woh already saved hai.

---

## Agar Kahin Atak Jayen

Jahan bhi rukein, bas yeh bata dein:
- Kaunsa Step number tha
- Screen par kya dikha (screenshot bhi bhej sakte hain)

Aur hum wahin se aage badhenge.
