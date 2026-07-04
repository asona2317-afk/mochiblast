"""
Middleware untuk otomatis mendaftarkan user ke database setiap kali
mereka berinteraksi dengan bot (message maupun callback query).
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject, User as TgUser

from bot.services.user_service import get_or_create_user
from bot.utils.logger import get_logger

logger = get_logger(__name__)


class UserRegistrationMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        tg_user: TgUser = data.get("event_from_user")

        if tg_user is not None and not tg_user.is_bot:
            try:
                await get_or_create_user(
                    telegram_id=tg_user.id,
                    username=tg_user.username,
                    fullname=tg_user.full_name,
                )
            except Exception:
                logger.exception("Gagal mendaftarkan/memperbarui user %s", tg_user.id)

        return await handler(event, data)
