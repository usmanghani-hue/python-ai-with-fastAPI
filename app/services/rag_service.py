"""
RAG service — the orchestrator. Given a user message, this:

1. Loads short-term conversation memory
2. Retrieves relevant knowledge (hybrid search)
3. Checks retrieval confidence against the configured threshold
4. Builds the grounded system prompt
5. Calls the LLM
6. Persists the exchange (messages table + short-term memory)

This is the single entrypoint both the WhatsApp webhook and the
test chat endpoint call — keeping behavior identical across channels.
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.models import Conversation, Message
from app.rag.prompt_builder import average_confidence, build_system_prompt
from app.rag.retriever import hybrid_search
from app.services import memory_service
from app.services.llm_service import generate_answer

settings = get_settings()

LOW_CONFIDENCE_FALLBACK = (
    "I don't have enough verified information to answer that accurately. "
    "Let me connect you with someone who can help."
)


async def answer_message(db: AsyncSession, conversation_id: uuid.UUID, user_message: str) -> tuple[str, float]:
    """Returns (answer_text, confidence_score)."""

    chunks = await hybrid_search(db, user_message)
    confidence = average_confidence(chunks)

    short_term = await memory_service.get_short_term(conversation_id)

    if confidence < settings.retrieval_confidence_threshold and not chunks:
        answer = LOW_CONFIDENCE_FALLBACK
    else:
        system_prompt = build_system_prompt(chunks)
        conversation_messages = short_term + [{"role": "user", "content": user_message}]
        answer = await generate_answer(system_prompt, conversation_messages)

    # Persist to DB
    db.add(Message(conversation_id=conversation_id, role="user", content=user_message))
    db.add(
        Message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
            retrieved_chunk_ids=[str(c.chunk_id) for c in chunks],
            confidence_score=confidence,
        )
    )
    await db.commit()

    # Update short-term memory
    await memory_service.append_short_term(conversation_id, "user", user_message)
    await memory_service.append_short_term(conversation_id, "assistant", answer)

    return answer, confidence


async def get_or_create_conversation(db: AsyncSession, user_id: uuid.UUID) -> Conversation:
    """
    MVP simplification: one active conversation per user. Multi-conversation
    threading (e.g. explicit "new topic") can be added later without
    changing this function's callers.
    """
    from sqlalchemy import select

    conversation = await db.scalar(
        select(Conversation)
        .where(Conversation.user_id == user_id, Conversation.status == "active")
        .order_by(Conversation.created_at.desc())
    )
    if conversation is None:
        conversation = Conversation(user_id=user_id, status="active")
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
    return conversation
