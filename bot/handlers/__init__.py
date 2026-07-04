from aiogram import Router

from bot.handlers.user import router as user_router
from bot.handlers.order import router as order_router
from bot.handlers.admin import router as admin_router
from bot.handlers.fallback import router as fallback_router


def get_main_router() -> Router:
    """Menggabungkan seluruh router menjadi satu router utama.

    Urutan include penting: fallback_router harus paling akhir supaya
    tidak menangkap update yang seharusnya ditangani router lain.
    """
    main_router = Router(name="main_router")

    main_router.include_router(admin_router)
    main_router.include_router(order_router)
    main_router.include_router(user_router)
    main_router.include_router(fallback_router)

    return main_router
