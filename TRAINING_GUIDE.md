# Chatbot Ko "Train" Karna — Documents Aur Chat History Ingest Karna

**Zaroori baat samajh lein:** Yeh chatbot LLM ko *retrain* nahi karta.
Iski jagah, "training" ka matlab hai: aapki knowledge (policies, FAQs,
approved chat history) ko database mein aise store karna ke jab user
sawal pooche, bot usay retrieve kar ke us par based answer de. Isay
**RAG (Retrieval-Augmented Generation)** kehte hain — jo hum ne
Architecture mein banaya hai.

Naya update karna ho (jaise price change, nayi policy) to bas naya
document ingest kar dein — LLM ko dobara train karne ki zaroorat nahi.

---

## Admin API Kaise Use Karein

Humara backend ek admin endpoint deta hai jahan text bhej kar knowledge
add ki ja sakti hai. Isay test karne ke do tareeqe hain:

### Option A — Swagger UI Se (Sabse Aasan, Koi Extra Tool Nahi Chahiye)

1. Server chalayein: `uvicorn app.main:app --reload --port 8000`
2. Browser mein kholein: `http://localhost:8000/docs`
3. Yeh FastAPI ka automatic interactive documentation page hai — yahan
   se seedha API call kar sakte hain.
4. **`POST /admin/documents/ingest-text`** endpoint dhoondhein → **"Try
   it out"** dabayein.
5. Upar right corner mein ek **"Authorize"** button bhi hoga (lock icon)
   — us par click kar ke `X-Admin-Key` mein wahi value daalein jo
   `.env` file mein `ADMIN_JWT_SECRET` ke against likhi hai.
6. Request body mein apni knowledge daalein, maslan:
   ```json
   {
     "title": "Germany Scholarship FAQ",
     "raw_text": "Germany scholarships ke liye students ko kam se kam 3.0 CGPA chahiye. IELTS 6.5 band score zaroori hai agar program English mein ho. Application deadline har saal 15 July hai.",
     "source_type": "faq",
     "category": "germany",
     "language": "roman-urdu",
     "priority": 1
   }
   ```
7. **"Execute"** dabayein. Response mein document ki details wapis
   milengi — matlab yeh content ab database mein chunk + embed ho kar
   store ho chuka hai aur retrieval ke liye ready hai.

### Option B — Command Line Se (curl)

```
curl -X POST http://localhost:8000/admin/documents/ingest-text ^
  -H "X-Admin-Key: aapki_admin_key" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Germany Scholarship FAQ\",\"raw_text\":\"...\",\"source_type\":\"faq\"}"
```
(Windows Command Prompt mein `^` line-break ke liye use hota hai.)

---

## Chat History Ingest Karna

Agar aapke paas purani human support conversations hain (WhatsApp
export, ya kisi CSV/text file mein), unhe is tarah ingest karein:

1. `source_type` ko `"chat_history"` set karein — is se hamara cleaning
   pipeline automatically greetings/filler lines ("hi", "thanks",
   "ok") remove kar dega, sirf useful Q&A rakhega.
2. `raw_text` mein poori conversation paste kar dein, jaisay:
   ```
   Customer: Germany mein masters ke liye kya requirements hain?
   Human: Germany ke liye aapko specific university aur program ki requirements check karni hongi. Generally 16 years education aur relevant bachelor's degree chahiye hoti hai.
   Customer: IELTS zaroori hai?
   Human: Zyada tar programs ke liye IELTS 6.0-6.5 chahiye hota hai, lekin kuch English-taught programs mein waiver bhi milta hai agar pichli degree English medium thi.
   ```
3. Yeh submit karein — system isay clean kar ke, chunks mein todd kar,
   embeddings bana kar store kar dega.

---

## Documents List Karna Aur Delete Karna

- **List:** `GET /admin/documents` (Swagger UI se ya curl se, same
  `X-Admin-Key` header ke saath)
- **Delete (deactivate):** `DELETE /admin/documents/{document_id}` —
  yeh document ko "inactive" mark kar deta hai, matlab bot ab usay
  retrieve nahi karega, lekin record delete nahi hota (audit ke liye
  rakha jata hai).

---

## Test Karna Ke Training Kaam Kar Rahi Hai

Ingest karne ke baad, WhatsApp se pehle, seedha test endpoint se check
kar sakte hain:

**`POST /chat/test`** (Swagger UI se, ya curl se):
```json
{
  "test_user_id": "tester1",
  "message": "Germany scholarship ke liye IELTS zaroori hai?"
}
```

Agar aap ne upar wali FAQ ingest ki thi, bot ka jawab usi information par
based hona chahiye — agar aisa nahi hai, to shayad ingestion mein kuch
masla hai (check karein document `status: active` hai ya nahi, `GET
/admin/documents` se).

---

## Priority Aur Category Ka Faida

- `priority: 1` = sabse zyada trust wali knowledge (official policy).
  `priority: 5` = kam trust wali (purani chat history). Retrieval abhi
  sirf relevance se rank karta hai — priority-based filtering future
  enhancement hai jo hum Phase 6 ko refine karte waqt add kar sakte
  hain agar zaroorat mehsoos ho.
- `category` se future mein filtering ki ja sakti hai (e.g. sirf
  "germany" category se retrieve karna) — abhi metadata ke tor par
  store ho raha hai.
