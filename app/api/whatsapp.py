"""
WhatsApp webhook routes.

GET  /webhook  — Meta's one-time verification handshake
POST /webhook  — incoming messages
"""

import structlog
from fastapi import APIRouter, Depends, Query, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.connection import get_db
from app.database.models import User
from app.services import rag_service, whatsapp_service

router = APIRouter()
settings = get_settings()
logger = structlog.get_logger()


@router.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    """Meta calls this once when you save the webhook URL in the App Dashboard."""
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_webhook_verify_token:
        return Response(content=hub_challenge, media_type="text/plain")
    return Response(status_code=403)


@router.post("/webhook")
async def receive_webhook(request: Request, db: AsyncSession = Depends(get_db)):
    raw_body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")

    if not whatsapp_service.verify_webhook_signature(raw_body, signature):
        logger.warning("webhook_signature_invalid")
        return Response(status_code=403)

    payload = await request.json()
    extracted = whatsapp_service.extract_incoming_message(payload)
    if extracted is None:
        # Non-text message or a status update — acknowledge and ignore.
        return {"status": "ignored"}

    from_number, text_body = extracted
    logger.info("whatsapp_message_received", from_number=from_number)

    # Find or create the user
    from sqlalchemy import select

    user = await db.scalar(select(User).where(User.whatsapp_number == from_number))
    if user is None:
        user = User(whatsapp_number=from_number)
        db.add(user)
        await db.commit()
        await db.refresh(user)

    conversation = await rag_service.get_or_create_conversation(db, user.id)
    answer, confidence = await rag_service.answer_message(db, conversation.id, text_body)

    await whatsapp_service.send_text_message(from_number, answer)

    return {"status": "ok", "confidence": confidence}
