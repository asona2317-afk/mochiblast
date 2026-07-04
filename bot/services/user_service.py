"""
Service untuk operasi terkait tabel `users`.
"""

from typing import Optional, Sequence

from sqlalchemy import func, select

from bot.database import get_session
from bot.models.user import User
from bot.utils.logger import get_logger

logger = get_logger(__name__)


async def get_or_create_user(
    telegram_id: int,
    username: Optional[str],
    fullname: Optional[str],
) -> User:
    """Mengambil user dari database, atau membuat baru jika belum ada."""
    async with get_session() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = User(
                telegram_id=telegram_id,
                username=username,
                fullname=fullname,
            )
            session.add(user)
            await session.flush()
            logger.info("User baru terdaftar: telegram_id=%s username=%s", telegram_id, username)
        else:
            # Update data terbaru jika ada perubahan username/fullname.
            updated = False
            if user.username != username:
                user.username = username
                updated = True
            if user.fullname != fullname:
                user.fullname = fullname
                updated = True
            if updated:
                session.add(user)

        return user


async def get_all_users() -> Sequence[User]:
    """Mengambil seluruh user yang terdaftar."""
    async with get_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()


async def count_total_users() -> int:
    """Menghitung total user terdaftar."""
    async with get_session() as session:
        result = await session.execute(select(func.count(User.id)))
        return result.scalar_one()
