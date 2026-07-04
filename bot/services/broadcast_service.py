"""
Service untuk mengirim broadcast ke seluruh user terdaftar.
"""

import asyncio
from dataclasses import dataclass

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter, TelegramBadRequest
from aiogram.types import Message

from bot.services.user_service import get_all_users
from bot.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class BroadcastResult:
    total: int
    success: int
    failed: int


async def broadcast_message(bot: Bot, source_message: Message) -> BroadcastResult:
    """
    Mengirim ulang (copy) sebuah pesan ke seluruh user terdaftar.
    Mendukung text, photo, video, document, dan animation karena
    menggunakan copy_to bawaan aiogram yang otomatis menangani semua
    jenis media tersebut.
    """
    users = await get_all_users()
    total = len(users)
    success = 0
    failed = 0

    for user in users:
        try:
            await source_message.copy_to(chat_id=user.telegram_id)
            success += 1
        except TelegramRetryAfter as exc:
            logger.warning("Terkena flood control, menunggu %s detik", exc.retry_after)
            await asyncio.sleep(exc.retry_after)
            try:
                await source_message.copy_to(chat_id=user.telegram_id)
                success += 1
            except Exception:
                failed += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            failed += 1
        except Exception as exc:
            logger.exception("Gagal mengirim broadcast ke %s: %s", user.telegram_id, exc)
            failed += 1

        # Jeda kecil supaya tidak terkena rate limit Telegram.
        await asyncio.sleep(0.05)

    logger.info("Broadcast selesai: total=%s sukses=%s gagal=%s", total, success, failed)
    return BroadcastResult(total=total, success=success, failed=failed)
