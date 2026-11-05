# Windows Guide — .env File Kaise Dhoondhein Aur Edit Karein

Yeh guide bilkul shuru se hai — maan kar chal rahe hain aapko pata nahi
kuch bhi. Step by step follow karein.

---

## Step 1 — Project Folder Dhoondhein

1. Jab aap ne `whatsapp-rag-bot-phase2.zip` download ki thi, woh normally
   **Downloads** folder mein jati hai.
2. **File Explorer** kholein (taskbar par folder icon, ya `Windows key + E`
   dabayein).
3. Left side se **Downloads** par click karein.
4. Wahan `whatsapp-rag-bot-phase2.zip` file dikhegi. Us par **right-click**
   karein → **"Extract All..."** → **"Extract"** button dabayein.
5. Ab ek nayi folder banegi: `whatsapp-rag-bot-phase2` (ya sirf
   `whatsapp-rag-bot`). Usay khol lein.
6. Andar `whatsapp-rag-bot` naam ki folder milegi (agar do folders nested
   hain) — usay khol lein. Yehi hamara **project root folder** hai. Isme
   `app`, `requirements.txt`, `README.md` waghera files nazar aani
   chahiye.

---

## Step 2 — File Extensions Dikhana ON Karein (Zaroori)

Windows default mein file extensions (`.txt`, `.md`, `.env`) chupa deta
hai, jis se confusion hoti hai. Pehle yeh on karein:

1. File Explorer mein upar **"View"** tab par click karein.
2. **"Show"** par click karein (ya seedha "Show" dropdown).
3. **"File name extensions"** checkbox ko tick karein.

Ab saari files ke naam ke aakhir mein `.md`, `.txt`, `.py` waghera nazar
aayenge — yeh zaroori hai taake hum `.env` file ko sahi tareeqay se
identify aur save kar sakein.

---

## Step 3 — `.env` File Banayein (Yeh Abhi Exist Nahi Karti)

**Zaroori baat:** Project mein `.env` naam ki file abhi maujood nahi hai —
sirf `.env.example` hai. Aapko `.env.example` ki **copy** banani hai aur
uska naam `.env` rakhna hai.

1. Project root folder mein `.env.example` file dhoondhein.
2. Us par **right-click** karein → **Copy**.
3. Khaali jagah par **right-click** karein → **Paste**. Ek nayi file banegi
   jiska naam kuch aisa hoga: `.env.example - Copy` ya `.env - Copy`.
4. Us nayi file par right-click karein → **Rename** → naam replace karke
   likhein:
   ```
   .env
   ```
   (Bas yeh 4 characters: dot, e, n, v — koi extension add nahi karna,
   `.env.txt` nahi banana.)
5. Enter dabayein. Windows kabhi warning dega "if you change file name
   extension..." — **"Yes"** kar dein.

Agar `.env` naam ki file banane mein dikkat aaye (Windows kabhi files jo
sirf dot se shuru hoti hain unko theek se rename nahi hone deta), to yeh
tarika try karein:
- File ka naam rakhein: `.env.` (aakhir mein ek extra dot lagayein) aur
  Enter dabayein — Windows woh aakhri dot khud hata dega aur sirf `.env`
  reh jayega.

---

## Step 4 — `.env` File Kholein Editing Ke Liye

**Normal Notepad se kholna** (sabse simple):
1. `.env` file par **right-click** karein.
2. **"Open with"** → **"Notepad"** select karein.
3. File khul jayegi — andar bahut sari lines dikhengi jaisay:
   ```
   DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/whatsapp_rag_bot
   REDIS_URL=redis://localhost:6379/0
   ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
   ```

**Behtar option (agar VS Code install hai):**
Agar aapke computer par **VS Code** installed hai, to poori project
folder (`whatsapp-rag-bot`) ko VS Code mein khol lein — left side sab
files ek list mein dikhengi, aur `.env` par click karke edit kar sakte
hain. Yeh zyada aasan hai kyunke saari files ek jagah nazar aati hain.

---

## Step 5 — `DATABASE_URL` Line Ko Replace Karein

Notepad mein `Ctrl + H` dabayein (Find & Replace), ya seedha us line ko
select karke delete kar dein aur nayi line type kar dein.

Neon se jo connection string aapko mili thi, woh kuch aisi thi:
```
postgresql://neondb_owner:PASSWORD@ep-broad-morning-axdjhpke.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require
```

Isay `.env` file mein daalte waqt **do cheezen change karni hain**:

1. Shuru mein `postgresql://` ki jagah `postgresql+asyncpg://` likhein
2. Aakhir mein `?sslmode=require` wala hissa **hata dein**

To `.env` file mein yeh line aisi honi chahiye (apna asli password daal
kar):

```
DATABASE_URL=postgresql+asyncpg://neondb_owner:AAPKA_ASLI_PASSWORD@ep-broad-morning-axdjhpke.c-4.us-east-2.aws.neon.tech/neondb
```

**Aapki asli string ka example:** Aap ne jo string bheji thi —
`postgresql://neondb_owner:npg_xxxx...@ep-broad-morning-axdjhpke.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require`
— usay `.env` mein daalte waqt **change karni hai, as-it-is nahi rakhni**.
Sirf yeh 2 changes karein:
1. Shuru mein `postgresql://` ko `postgresql+asyncpg://` banayein
2. Aakhir mein `?sslmode=require` wala hissa **poora hata dein**

Baaki sab (username, password, host, database name) bilkul waisa hi
rehne dein jaisa Neon ne diya tha.

**Password kahan se milega?** Neon ke dashboard par jo screenshot aap ne
bheja tha, wahan "Show password" button dabayein — tab asli password
nazar aayega (abhi stars `***` dikha raha tha). Wahi copy karke upar wali
line mein `AAPKA_ASLI_PASSWORD` ki jagah paste karein.

---

## Step 6 — Baaki Values Bhi Samajhein (Filhaal Chorr Sakte Hain)

Neeche di gayi values abhi ke liye waise hi rehne dein (placeholder), jab
tak WhatsApp/LLM part par nahi pahunchte:

```
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
WHATSAPP_ACCESS_TOKEN=xxxxxxxxxxxxxxxxxxxxx
```

Sirf yeh do zaroori hain abhi (koi bhi random text daal dein, bas empty
na ho):
```
APP_SECRET_KEY=mySecretKey12345
ADMIN_JWT_SECRET=myAdminSecret12345
```

`REDIS_URL` abhi purani wali (`redis://localhost:6379/0`) rehne dein —
jab Upstash bana lenge to isay bhi replace karenge.

---

## Step 7 — File Save Karein

1. Notepad mein **`Ctrl + S`** dabayein (Save).
2. Agar "Save As" window khule aur file type `.txt` dikhaye, to type
   dropdown mein **"All Files"** select karein taake `.env.txt` na ban
   jaye — file ka naam sirf `.env` hi rehna chahiye.

---

## Step 8 — Confirm Karein File Sahi Bani Hai

File Explorer mein wapis project folder mein check karein:
- File ka naam sirf `.env` hona chahiye (`.env.txt` nahi)
- Same folder mein `.env.example`, `app`, `requirements.txt` bhi dikhne
  chahiye

---

## Step 9 — Python Install Karein (Agar Pehle Se Nahi Hai)

1. Check karein ke Python pehle se installed hai ya nahi. **Start menu**
   kholein, type karein `cmd`, Enter dabayein — ek black window
   (Command Prompt) khulegi. Usme likhein:
   ```
   python --version
   ```
   Agar kuch aisa dikhe `Python 3.12.x` — matlab already installed hai,
   Step 10 par chalein jayein.

2. Agar error aaye ya "not recognized" likha aaye, to Python install
   karna hoga:
   - [python.org/downloads](https://www.python.org/downloads/) par
     jaayein aur **latest Python 3.12** download karein.
   - Installer chalate waqt sabse pehle screen par neeche **"Add python.exe
     to PATH"** checkbox zaroor tick karein — yeh bohat zaroori hai,
     warna aage commands kaam nahi karengi.
   - **"Install Now"** dabayein.
   - Installation ke baad Command Prompt band karke dobara kholein, aur
     `python --version` se check karein.

---

## Step 10 — Command Prompt Ko Project Folder Mein Le Jaayein

Command Prompt mein `cd` (change directory) command se project folder
tak pahunchna hai. Maslan agar project `Downloads` mein hai:

```
cd Downloads\whatsapp-rag-bot-phase2\whatsapp-rag-bot
```

(Apne actual folder path ke hisaab se adjust karein — path File
Explorer ke address bar se bhi copy ho sakta hai.)

Confirm karne ke liye likhein:
```
dir
```
Yeh current folder ki files list karega — `app`, `requirements.txt`,
`.env` waghera dikhne chahiye. Agar yeh dikh rahi hain, matlab aap sahi
jagah par hain.

---

## Step 11 — Virtual Environment Banayein

Yeh ek "isolated box" hota hai jahan is project ki Python libraries
alag se install hoti hain, taake system ki doosri cheezon se clash na
ho.

```
python -m venv .venv
```

Yeh command kuch second lagayegi, aur `.venv` naam ki ek folder ban
jayegi.

---

## Step 12 — Virtual Environment Activate Karein

```
.venv\Scripts\activate
```

Agar sahi se chala, to Command Prompt line ke shuru mein `(.venv)`
likha nazar aayega, jaisay:
```
(.venv) C:\Users\YourName\Downloads\whatsapp-rag-bot-phase2\whatsapp-rag-bot>
```

**Yeh har baar karna hoga** jab bhi naya Command Prompt window kholein
aur project par kaam karna ho.

---

## Step 13 — Libraries Install Karein

`(.venv)` active hone ke baad:

```
pip install -r requirements.txt
```

Yeh command thora time legi (1-3 minute) — bohat sari libraries download
aur install hongi. Terminal mein neeche tak scroll hote hue "Successfully
installed..." dikhega jab complete ho jaye.

---

## Step 14 — Server Start Karein

```
uvicorn app.main:app --reload --port 8000
```

Agar sab sahi hai, to yeh dikhega:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

Is window ko **band na karein** — jab tak yeh khuli hai, server chal
raha hai. Band karne ke liye `Ctrl + C` dabayein.

---

## Step 15 — Browser Mein Check Karein

Naya Command Prompt window nahi, seedha **browser** kholein (Chrome/Edge)
aur yeh address type karein:

```
http://localhost:8000/health
```

Yeh dikhna chahiye:
```json
{"status": "ok", "env": "development"}
```

Agar yeh mil gaya — **server successfully chal raha hai**, database
(Neon) se bhi connected hai.

---

## Common Errors Is Stage Par

| Error | Wajah | Hal |
|---|---|---|
| `'uvicorn' is not recognized` | `.venv` activate nahi hai | Step 12 dobara karein |
| `python is not recognized` | Python install ke waqt PATH checkbox tick nahi hua tha | Python dobara install karein, PATH wala checkbox tick karein |
| Server start hote hi crash ho jaye, database error dikhaye | `.env` mein `DATABASE_URL` galat hai | Step 5 dobara check karein — `+asyncpg` aur `?sslmode=require` hatana na bhoolein |
| `pip install` mein error | Internet connection ya kisi package ka issue | Error message ka screenshot bhej dein |

---

## Agla Kadam

Yahan tak backend successfully chal raha hai, Neon database se connected
hai. Agle mein hum database tables banayenge (Phase 4) aur phir asal
chatbot logic (RAG, WhatsApp) par kaam shuru karenge.

Agar kahin bhi atak jayein — file na mile, koi command error de, ya koi
screenshot mein confusion ho, to bas screenshot bhej dein aur bata dein
kahan atke hain.
