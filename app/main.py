"""
FastAPI application entrypoint.

Run locally with:
    uvicorn app.main:app --reload --port 8000
"""

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.admin import router as admin_router
from app.api.chat import router as chat_router
from app.api.whatsapp import router as whatsapp_router
from app.config import get_settings
from app.database.connection import init_db

settings = get_settings()

logger = structlog.get_logger()

app = FastAPI(
    title="WhatsApp RAG Chatbot",
    description="Production-ready RAG-based WhatsApp chatbot",
    version="0.1.0",
)

# CORS — tighten allow_origins in production to the admin panel's real domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if not settings.is_production else [],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    """Enables pgvector and creates tables if they don't exist yet."""
    await init_db()
    logger.info("app_startup", env=settings.app_env)


@app.get("/health")
async def health_check():
    """Basic liveness probe — used by hosting platform / uptime monitors."""
    return {"status": "ok", "env": settings.app_env}


app.include_router(whatsapp_router, tags=["whatsapp"])
app.include_router(chat_router, prefix="/chat", tags=["chat"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])