"""
Async database engine, session factory, and a simple startup routine
that enables pgvector and creates tables.

For the MVP we use `Base.metadata.create_all` instead of Alembic
migrations to keep local setup simple. Once the schema stabilizes,
switch to Alembic (`alembic init`) for versioned migrations before
production launch — create_all() cannot handle schema changes safely.
"""

from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.engine import URL, make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import get_settings
from app.database.models import Base

settings = get_settings()

def _database_engine_options(database_url: str) -> tuple[URL, dict[str, object]]:
    """Adapt provider URLs such as Neon URLs for asyncpg."""
    url = make_url(database_url)
    query = dict(url.query)
    connect_args: dict[str, object] = {}

    # sslmode/channel_binding are libpq options. asyncpg expects TLS in
    # connect_args and does not accept these options as URL query values.
    sslmode = query.pop("sslmode", None)
    query.pop("channel_binding", None)
    if sslmode in {"require", "verify-ca", "verify-full"}:
        connect_args["ssl"] = "require"

    return url.set(query=query), connect_args


database_url, database_connect_args = _database_engine_options(settings.database_url)
engine = create_async_engine(
    database_url,
    connect_args=database_connect_args,
    echo=False,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency — yields a DB session per request."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    """
    Enable the pgvector extension and create all tables that don't
    already exist. Safe to call every startup — it's a no-op if the
    schema is already in place.
    """
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
