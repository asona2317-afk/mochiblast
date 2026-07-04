"""
Inline keyboard untuk menu customer.
"""

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.config import settings
from bot.keyboards import callback_data as cb


def main_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📋 Pricelist", callback_data=cb.MENU_PRICELIST)
    builder.button(text="🛒 Order", callback_data=cb.MENU_PRICELIST)
    builder.button(text="📖 Cara Order", callback_data=cb.MENU_CARA_ORDER)
    builder.button(text="⭐ Keunggulan", callback_data=cb.MENU_KEUNGGULAN)
    builder.button(text="👩‍💼 Admin", callback_data=cb.MENU_ADMIN)
    builder.button(text="📢 Channel", callback_data=cb.MENU_CHANNEL)
    builder.adjust(2, 2, 2)
    return builder.as_markup()


def pricelist_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="☁️ Mochi Basic", callback_data=cb.PRICELIST_BASIC)
    builder.button(text="👑 Mochi Premium", callback_data=cb.PRICELIST_PREMIUM)
    builder.button(text="⬅️ Kembali", callback_data=cb.MENU_MAIN)
    builder.adjust(1, 1, 1)
    return builder.as_markup()


def package_detail_kb(paket: str) -> InlineKeyboardMarkup:
    """Keyboard untuk halaman detail paket (Basic/Premium)."""
    builder = InlineKeyboardBuilder()
    if paket == "basic":
        builder.button(text="🛒 Order Basic", callback_data=cb.ORDER_START_BASIC)
    else:
        builder.button(text="🛒 Order Premium", callback_data=cb.ORDER_START_PREMIUM)
    builder.button(text="⬅️ Kembali", callback_data=cb.MENU_PRICELIST)
    builder.adjust(1, 1)
    return builder.as_markup()


def back_to_main_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Kembali", callback_data=cb.MENU_MAIN)
    return builder.as_markup()


def admin_contact_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="💬 Hubungi Admin",
        url=f"https://t.me/{settings.admin_username}",
    )
    builder.button(text="⬅️ Kembali", callback_data=cb.MENU_MAIN)
    builder.adjust(1, 1)
    return builder.as_markup()


def channel_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="📢 Join Channel", url=settings.channel_url)
    builder.button(text="⬅️ Kembali", callback_data=cb.MENU_MAIN)
    builder.adjust(1, 1)
    return builder.as_markup()


def durasi_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    opsi = ["3 Hari", "5 Hari", "7 Hari", "1 Bulan"]
    for opsi_durasi in opsi:
        builder.button(
            text=opsi_durasi,
            callback_data=f"{cb.ORDER_DURASI_PREFIX}{opsi_durasi}",
        )
    builder.button(text="❌ Batal", callback_data=cb.ORDER_CANCEL)
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def jumlah_lpm_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    opsi = ["10 Grup/LPM", "20 Grup/LPM", "30 Grup/LPM"]
    for opsi_lpm in opsi:
        builder.button(
            text=opsi_lpm,
            callback_data=f"{cb.ORDER_LPM_PREFIX}{opsi_lpm}",
        )
    builder.button(text="❌ Batal", callback_data=cb.ORDER_CANCEL)
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def skip_request_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⏭️ Tidak Ada Request", callback_data=cb.ORDER_SKIP_REQUEST)
    builder.button(text="❌ Batal", callback_data=cb.ORDER_CANCEL)
    builder.adjust(1, 1)
    return builder.as_markup()


def confirmation_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Kirim", callback_data=cb.ORDER_CONFIRM)
    builder.button(text="❌ Batal", callback_data=cb.ORDER_CANCEL)
    builder.adjust(2)
    return builder.as_markup()
