"""
Pengaturan koneksi database (SQLAlchemy Async Engine + Session Factory).
"""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.config import settings
from bot.models.base import Base
from bot.utils.logger import get_logger

logger = get_logger(__name__)

engine = create_async_engine(settings.database_url, echo=False, future=True)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def init_db() -> None:
    """Membuat seluruh tabel jika belum ada."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database berhasil diinisialisasi.")


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """Context manager untuk mendapatkan sesi database yang aman."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
