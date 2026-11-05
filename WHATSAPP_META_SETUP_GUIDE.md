# WhatsApp Cloud API Setup — Meta Developer Console

Yeh steps sirf aap khud kar sakte hain, kyunke yeh aapke Facebook/Meta
account se juri hain. Code taiyar hai, bas yeh credentials chahiye.

---

## Step 1 — Meta Developer Account Banayein

1. [developers.facebook.com](https://developers.facebook.com) par
   jaayein, apne Facebook account se login karein.
2. Upar right corner **"My Apps"** → **"Create App"**.
3. App type mein **"Business"** select karein → **"Next"**.
4. App ka naam de dein (kuch bhi, jaise "Dynamite Support Bot") →
   **"Create App"**.

---

## Step 2 — WhatsApp Product Add Karein

1. App Dashboard mein neeche scroll karein, **"WhatsApp"** product
   dhoondh kar **"Set up"** dabayein.
2. Ab aapko ek **test phone number** mil jayega (Meta free mein deta hai
   testing ke liye) — production mein baad mein apna number add kar
   sakte hain.

---

## Step 3 — Zaroori Values Nikalein

WhatsApp → **"API Setup"** page par yeh sab milega:

| `.env` Variable | Kahan Se Milega |
|---|---|
| `WHATSAPP_PHONE_NUMBER_ID` | "Phone number ID" field ke neeche |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Same page par "WhatsApp Business Account ID" |
| `WHATSAPP_ACCESS_TOKEN` | "Temporary access token" — 24 ghante ke liye valid hota hai (testing ke liye theek hai) |
| `WHATSAPP_APP_SECRET` | App Dashboard → **Settings → Basic** → "App Secret" (Show dabana hoga) |

Yeh sab `.env` file mein daal dein.

> **Permanent token (production ke liye):** Temporary token 24 ghante
> baad expire ho jata hai. Jab production par jaana ho, System User se
> permanent token banana hoga: Business Settings → System Users → naya
> system user banayein → WhatsApp app assign karein → token generate
> karein with `whatsapp_business_messaging` permission.

---

## Step 4 — Webhook Verify Token Banayein

`.env` mein `WHATSAPP_WEBHOOK_VERIFY_TOKEN` ki value **aap khud** koi
bhi random string bana kar likh dein, maslan:
```
WHATSAPP_WEBHOOK_VERIFY_TOKEN=mySecretToken2026
```
Yeh sirf aapko aur Meta ko pata hoga — kisi API se nahi milta.

---

## Step 5 — Backend Ko Public URL Par Le Aayein

Meta ka webhook sirf **public HTTPS URL** par call kar sakta hai —
`localhost` kaam nahi karega. Do options hain:

### Option A — Testing Ke Liye: ngrok
1. [ngrok.com](https://ngrok.com) se free account banayein aur ngrok
   install karein.
2. Apna backend local chalayein (`uvicorn app.main:app --port 8000`).
3. Doosri terminal mein:
   ```
   ngrok http 8000
   ```
4. Yeh ek URL dega jaisay `https://abcd1234.ngrok-free.app` — yehi
   aapka temporary public URL hai.

### Option B — Production Ke Liye: Cloud Deploy
Render/Railway par backend deploy karein — woh khud hi public HTTPS URL
de dete hain (Phase 12 — Deployment guide alag se banayenge jab yahan
tak pahunchein).

---

## Step 6 — Webhook Meta Mein Configure Karein

1. WhatsApp → **"Configuration"** page par jaayein.
2. **"Edit"** (Webhook section) dabayein.
3. **Callback URL** mein daalein:
   ```
   https://aapka-public-url.com/webhook/webhook
   ```
   (Humare code mein route `/webhook` prefix ke andar `/webhook` hai,
   is liye poora path `/webhook/webhook` banta hai.)
4. **Verify Token** mein wahi likhein jo Step 4 mein `.env` mein daala
   tha (`mySecretToken2026`).
5. **"Verify and Save"** dabayein — agar sab sahi hai, Meta green tick
   dega.
6. Neeche **"Webhook fields"** mein **"messages"** field ko **Subscribe**
   karein — is ke bagair incoming messages nahi aayenge.

---

## Step 7 — Test Karein

1. Apne phone se us test WhatsApp number par message bhejein jo Step 2
   mein mila tha (pehle apna number "Recipient" list mein add karna
   hoga — WhatsApp → API Setup page par "To" field ke neeche "Manage
   phone number list").
2. Agar sab sahi setup hai, aapka backend terminal mein
   `whatsapp_message_received` log dikhega, aur kuch second mein bot
   ka reply WhatsApp par aa jayega.

---

## Common Errors

| Error | Wajah | Hal |
|---|---|---|
| Webhook verify fail ho | Verify token match nahi kar raha | `.env` aur Meta dashboard dono mein same token check karein |
| Message aaya hi nahi backend tak | "messages" field subscribe nahi hai | Step 6 ka aakhri part dobara karein |
| Reply nahi aa raha WhatsApp par | Access token expire ho gaya (24hr wala) | Naya temporary token le lein, ya permanent bana lein |
| `403` webhook POST par | Signature verify fail ho rahi hai | `.env` mein `WHATSAPP_APP_SECRET` sahi hai check karein |
