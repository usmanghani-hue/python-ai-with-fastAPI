"""
Admin API — upload knowledge (documents, FAQs, approved chat history),
list what's stored, and deactivate outdated documents.

Auth: MVP simplification — a single shared admin key checked via the
X-Admin-Key header, instead of full JWT user accounts. This is
sufficient for one-person or small-team admin use. Swap in real JWT
login (see ADMIN_JWT_SECRET in config) before opening this up to
multiple admin users.
"""

import uuid

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database.connection import get_db
from app.database.models import Document
from app.services.ingestion_service import deactivate_document, ingest_text

router = APIRouter()
settings = get_settings()


def require_admin_key(x_admin_key: str = Header(...)) -> None:
    if x_admin_key != settings.admin_jwt_secret:
        raise HTTPException(status_code=401, detail="Invalid admin key")


class IngestTextRequest(BaseModel):
    title: str
    raw_text: str
    source_type: str  # "pdf" | "docx" | "txt" | "csv" | "chat_history" | "faq"
    category: str | None = None
    language: str | None = None
    priority: int = 3


class DocumentOut(BaseModel):
    id: uuid.UUID
    title: str
    source_type: str
    category: str | None
    status: str
    priority: int

    class Config:
        from_attributes = True


@router.post("/documents/ingest-text", response_model=DocumentOut, dependencies=[Depends(require_admin_key)])
async def upload_text_knowledge(request: IngestTextRequest, db: AsyncSession = Depends(get_db)):
    """
    Ingest raw text as a new knowledge document. This is how you
    "train" the bot on company policies, FAQs, or approved chat
    history — paste the cleaned content here and it becomes
    retrievable knowledge immediately.
    """
    document = await ingest_text(
        db,
        title=request.title,
        raw_text=request.raw_text,
        source_type=request.source_type,
        category=request.category,
        language=request.language,
        priority=request.priority,
    )
    return document


@router.get("/documents", response_model=list[DocumentOut], dependencies=[Depends(require_admin_key)])
async def list_documents(db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(Document).order_by(Document.created_at.desc()))
    return result.all()


@router.delete("/documents/{document_id}", dependencies=[Depends(require_admin_key)])
async def delete_document(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    await deactivate_document(db, document_id)
    return {"status": "deactivated"}
