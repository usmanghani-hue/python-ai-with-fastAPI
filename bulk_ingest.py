"""
bulk_ingest.py — Splits an exported WhatsApp chat log (multi-chat format)
into per-conversation documents, removes personal info (phone/email/DOB),
and ingests each conversation into the RAG chatbot's knowledge base via
the admin API.

Usage (project root, venv active, server running on port 8000):
    python bulk_ingest.py whatsapp-export-combined.txt

Before running: set ADMIN_KEY below to match your .env's ADMIN_JWT_SECRET.
"""

import re
import sys
import httpx

BASE_URL = "http://localhost:8000"
ADMIN_KEY = "MySecretKey2026SirMuazamTheGreat"  # <-- .env se ADMIN_JWT_SECRET copy karo

# Tag every document from this run with this category — lets you filter
# knowledge per-agent later (e.g. "italy" for Ayesha, "france" for Ali).
CATEGORY = "italy"
TITLE_PREFIX = "Ayesha - Italy"

# --- Privacy: strip personal info before it becomes searchable knowledge ---
PHONE_RE = re.compile(r"\+?\d[\d\-\s]{8,}\d")
EMAIL_RE = re.compile(r"[\w.\-]+@[\w.\-]+\.\w+")
DOB_RE = re.compile(r"\b(0[1-9]|1[0-2])[/-](0[1-9]|[12]\d|3[01])[/-](19|20)\d{2}\b")
DOB_ISO_RE = re.compile(r"\b(19|20)\d{2}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b")


def scrub(text: str) -> str:
    text = PHONE_RE.sub("[phone removed]", text)
    text = EMAIL_RE.sub("[email removed]", text)
    text = DOB_RE.sub("[date removed]", text)
    text = DOB_ISO_RE.sub("[date removed]", text)
    return text


def split_chats(raw: str):
    blocks = re.split(r"={10,}\nCHAT: (.+?)\n={10,}\n", raw)
    chats = []
    for i in range(1, len(blocks), 2):
        title = blocks[i].strip()
        body = blocks[i + 1].strip()
        body = body.split("=" * 10)[0].strip()  # cut off at next separator/footer
        if body and "END OF EXPORT" not in body:
            chats.append((title, body))
    return chats


def main(path: str):
    raw = open(path, encoding="utf-8").read()
    chats = split_chats(raw)
    print(f"Found {len(chats)} conversations.\n")

    ingested, skipped, failed = 0, 0, 0

    with httpx.Client(timeout=60) as client:
        for i, (title, body) in enumerate(chats, 1):
            cleaned_body = scrub(body)
            if len(cleaned_body) < 40:
                print(f"[{i}/{len(chats)}] Skipping '{title}' (too short/empty).")
                skipped += 1
                continue

            payload = {
                "title": f"{TITLE_PREFIX} - {title}",
                "raw_text": cleaned_body,
                "source_type": "chat_history",
                "category": CATEGORY,
                "language": None,
                "priority": 3,
            }
            resp = client.post(
                f"{BASE_URL}/admin/documents/ingest-text",
                headers={"x-admin-key": ADMIN_KEY},
                json=payload,
            )
            if resp.status_code == 200:
                print(f"[{i}/{len(chats)}] Ingested: {title}")
                ingested += 1
            else:
                print(f"[{i}/{len(chats)}] FAILED ({resp.status_code}): {title} -> {resp.text[:150]}")
                failed += 1

    print(f"\nDone. Ingested: {ingested} | Skipped: {skipped} | Failed: {failed}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python bulk_ingest.py path/to/export.txt")
        sys.exit(1)
    main(sys.argv[1])