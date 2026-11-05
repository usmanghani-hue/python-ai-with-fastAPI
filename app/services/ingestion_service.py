"""
Ingestion service — turns raw documents / approved chat history into
searchable knowledge. This IS the "training" step referred to in the
project spec: nothing here retrains the LLM; it populates the
retrieval database that the LLM is grounded on at answer time.

Pipeline: clean -> chunk -> embed -> store (with metadata).
"""

import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Document, DocumentChunk
from app.rag.chunking import chunk_text
from app.services.embedding_service import embed_batch
from app.utils.text_cleaning import basic_clean, clean_chat_history


async def ingest_text(
    db: AsyncSession,
    *,
    title: str,
    raw_text: str,
    source_type: str,  # "pdf" | "docx" | "txt" | "csv" | "chat_history" | "faq"
    category: str | None = None,
    language: str | None = None,
    priority: int = 3,
) -> Document:
    """
    Ingest a single piece of text as a new Document, chunked and
    embedded. Call this from the admin upload endpoint, or from a
    batch script when importing historical chat exports.
    """
    cleaned = clean_chat_history(raw_text) if source_type == "chat_history" else basic_clean(raw_text)

    chunks = chunk_text(cleaned)
    if not chunks:
        raise ValueError("No content left to ingest after cleaning — check the input text.")

    embeddings = await embed_batch(chunks)

    document = Document(
        id=uuid.uuid4(),
        title=title,
        source_type=source_type,
        category=category,
        language=language,
        priority=priority,
        status="active",
    )
    db.add(document)
    await db.flush()  # get document.id before creating chunks

    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings, strict=True)):
        db.add(
            DocumentChunk(
                id=uuid.uuid4(),
                document_id=document.id,
                chunk_text=chunk,
                embedding=embedding,
                chunk_index=idx,
            )
        )

    await db.commit()
    await db.refresh(document)
    return document


async def deactivate_document(db: AsyncSession, document_id: uuid.UUID) -> None:
    """Soft-delete: marks inactive so it drops out of retrieval, without losing history."""
    document = await db.get(Document, document_id)
    if document:
        document.status = "inactive"
        await db.commit()
