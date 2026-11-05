"""
Memory service.

Short-term: last N turns of the active conversation, kept in Redis
with a TTL — used only for coreference resolution within a session
(e.g. "my CGPA is 3.4" -> later question about scholarships).

Long-term: a small set of structured fields per user, kept in
Postgres (`user_memory` table). Never free-text. Deletable on request.
"""

import json
import uuid

import redis.asyncio as redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.models import UserMemory

settings = get_settings()
_redis = redis.from_url(settings.redis_url, decode_responses=True)

SHORT_TERM_TTL_SECONDS = 60 * 60 * 6  # 6 hours of inactivity clears the short-term window
SHORT_TERM_MAX_TURNS = 12


def _short_term_key(conversation_id: uuid.UUID) -> str:
    return f"conv:{conversation_id}:messages"


async def append_short_term(conversation_id: uuid.UUID, role: str, content: str) -> None:
    key = _short_term_key(conversation_id)
    await _redis.rpush(key, json.dumps({"role": role, "content": content}))
    await _redis.ltrim(key, -SHORT_TERM_MAX_TURNS, -1)
    await _redis.expire(key, SHORT_TERM_TTL_SECONDS)


async def get_short_term(conversation_id: uuid.UUID) -> list[dict]:
    key = _short_term_key(conversation_id)
    raw_items = await _redis.lrange(key, 0, -1)
    return [json.loads(item) for item in raw_items]


async def clear_short_term(conversation_id: uuid.UUID) -> None:
    await _redis.delete(_short_term_key(conversation_id))


# --- Long-term memory (Postgres) ---

async def get_long_term(db: AsyncSession, user_id: uuid.UUID) -> UserMemory | None:
    return await db.scalar(select(UserMemory).where(UserMemory.user_id == user_id))


async def upsert_long_term(db: AsyncSession, user_id: uuid.UUID, **fields) -> UserMemory:
    """
    fields may include: education_level, field_of_study, preferred_country, intended_degree.
    Only known, structured fields are ever stored here.
    """
    memory = await get_long_term(db, user_id)
    if memory is None:
        memory = UserMemory(user_id=user_id, **fields)
        db.add(memory)
    else:
        for key, value in fields.items():
            setattr(memory, key, value)
    await db.commit()
    await db.refresh(memory)
    return memory


async def delete_long_term(db: AsyncSession, user_id: uuid.UUID) -> None:
    """User-requested deletion of all stored long-term memory."""
    memory = await get_long_term(db, user_id)
    if memory:
        await db.delete(memory)
        await db.commit()
