"""
Middleware untuk menangani error yang tidak tertangani di handler manapun,
supaya bot tidak crash dan customer/admin tetap mendapat feedback yang jelas.
"""

from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject

from bot.utils.logger import get_logger

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception as exc:
            logger.exception("Terjadi error saat memproses event: %s", exc)

            error_message = (
                "⚠️ Maaf, terjadi kesalahan pada sistem.\n"
                "Silakan coba lagi beberapa saat lagi atau hubungi admin."
            )

            try:
                if isinstance(event, Message):
                    await event.answer(error_message)
                elif isinstance(event, CallbackQuery):
                    await event.answer(error_message, show_alert=True)
                    if event.message:
                        await event.message.answer(error_message)
            except Exception:
                logger.exception("Gagal mengirim pesan error ke user.")

            return None
