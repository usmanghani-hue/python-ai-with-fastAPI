"""
WhatsApp Cloud API service — sending outbound messages and parsing
inbound webhook payloads. Uses the official Meta Graph API only.
"""

import hashlib
import hmac

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings

settings = get_settings()

GRAPH_API_BASE = f"https://graph.facebook.com/{settings.whatsapp_api_version}"


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
async def send_text_message(to_number: str, body: str) -> dict:
    url = f"{GRAPH_API_BASE}/{settings.whatsapp_phone_number_id}/messages"
    headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": body},
    }
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()


def verify_webhook_signature(payload_bytes: bytes, signature_header: str | None) -> bool:
    """
    Verifies Meta's X-Hub-Signature-256 header against WHATSAPP_APP_SECRET.
    Reject any webhook call that fails this check.
    """
    if not signature_header or not signature_header.startswith("sha256="):
        return False
    expected = hmac.new(
        settings.whatsapp_app_secret.encode(), payload_bytes, hashlib.sha256
    ).hexdigest()
    provided = signature_header.removeprefix("sha256=")
    return hmac.compare_digest(expected, provided)


def extract_incoming_message(payload: dict) -> tuple[str, str] | None:
    """
    Pulls (from_number, message_text) out of a WhatsApp webhook POST body.
    Returns None for non-message events (delivery receipts, status
    updates, etc.) — those should be acknowledged but not answered.
    """
    try:
        entry = payload["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        messages = value.get("messages")
        if not messages:
            return None
        message = messages[0]
        if message.get("type") != "text":
            return None
        from_number = message["from"]
        text_body = message["text"]["body"]
        return from_number, text_body
    except (KeyError, IndexError, TypeError):
        return None
