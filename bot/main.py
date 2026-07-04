"""
Entry point utama Mochi Blast Bot.

Jalankan file ini untuk memulai bot dalam mode polling:
    python -m bot.main
"""

import asyncio

from bot.database import init_db
from bot.handlers import get_main_router
from bot.loader import bot, dp
from bot.middlewares import ErrorHandlerMiddleware, UserRegistrationMiddleware
from bot.utils.logger import get_logger, setup_logging

logger = get_logger(__name__)


def setup_middlewares() -> None:
    """Mendaftarkan seluruh middleware global."""
    dp.update.outer_middleware(ErrorHandlerMiddleware())
    dp.message.middleware(UserRegistrationMiddleware())
    dp.callback_query.middleware(UserRegistrationMiddleware())


def setup_routers() -> None:
    """Mendaftarkan seluruh router (handler) ke dispatcher."""
    dp.include_router(get_main_router())


async def on_startup() -> None:
    logger.info("Menginisialisasi database...")
    await init_db()
    logger.info("Bot Mochi Blast siap berjalan.")


async def main() -> None:
    setup_logging()
    logger.info("Memulai Mochi Blast Bot...")

    setup_middlewares()
    setup_routers()

    await on_startup()

    # Pastikan tidak ada webhook aktif sebelum menjalankan polling.
    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot dihentikan.")
