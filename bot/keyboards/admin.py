"""
Inline keyboard untuk panel admin.
"""

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.keyboards import callback_data as cb


def admin_panel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 Statistik", callback_data=cb.ADMIN_STATS)
    builder.button(text="📦 Order Masuk", callback_data=cb.ADMIN_ORDERS)
    builder.button(text="📢 Broadcast", callback_data=cb.ADMIN_BROADCAST)
    builder.button(text="👥 Total User", callback_data=cb.ADMIN_USERS)
    builder.button(text="⚙ Pengaturan", callback_data=cb.ADMIN_SETTINGS)
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def back_to_admin_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Kembali", callback_data=cb.ADMIN_PANEL)
    return builder.as_markup()


def orders_pagination_kb(current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if current_page > 1:
        builder.button(
            text="⬅️ Sebelumnya",
            callback_data=f"{cb.ADMIN_ORDERS_PAGE_PREFIX}{current_page - 1}",
        )
    if current_page < total_pages:
        builder.button(
            text="Selanjutnya ➡️",
            callback_data=f"{cb.ADMIN_ORDERS_PAGE_PREFIX}{current_page + 1}",
        )
    builder.button(text="⬅️ Kembali ke Panel", callback_data=cb.ADMIN_PANEL)
    builder.adjust(2, 1)
    return builder.as_markup()


def broadcast_confirmation_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Kirim Broadcast", callback_data=cb.BROADCAST_CONFIRM)
    builder.button(text="❌ Batal", callback_data=cb.BROADCAST_CANCEL)
    builder.adjust(2)
    return builder.as_markup()
