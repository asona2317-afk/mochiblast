"""
Handler untuk seluruh fitur admin: panel admin, statistik, order masuk,
broadcast, total user, pengaturan, dan mekanisme reply order ke customer.
"""

import re

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.keyboards import callback_data as cb
from bot.keyboards.admin import (
    admin_panel_kb,
    back_to_admin_kb,
    broadcast_confirmation_kb,
    orders_pagination_kb,
)
from bot.services.broadcast_service import broadcast_message
from bot.services.order_service import count_orders_today, count_total_orders, get_orders_page
from bot.services.user_service import count_total_users
from bot.states.broadcast import BroadcastState
from bot.utils import texts
from bot.utils.logger import get_logger
from bot.utils.text import format_datetime, safe_html

router = Router(name="admin_router")
logger = get_logger(__name__)

ORDERS_PER_PAGE = 5

# Filter khusus untuk memastikan hanya admin yang bisa mengakses handler ini.
router.message.filter(F.from_user.id.in_(settings.admin_ids))
router.callback_query.filter(F.from_user.id.in_(settings.admin_ids))


@router.message(Command("admin"))
async def cmd_admin(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.ADMIN_PANEL_TEXT, reply_markup=admin_panel_kb())


@router.callback_query(F.data == cb.ADMIN_PANEL)
async def cb_admin_panel(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(texts.ADMIN_PANEL_TEXT, reply_markup=admin_panel_kb())
    await callback.answer()


@router.callback_query(F.data == cb.ADMIN_STATS)
async def cb_admin_stats(callback: CallbackQuery) -> None:
    total_user = await count_total_users()
    total_order = await count_total_orders()
    order_hari_ini = await count_orders_today()

    text = texts.ADMIN_STATS_TEMPLATE.format(
        total_user=total_user,
        total_order=total_order,
        order_hari_ini=order_hari_ini,
    )
    await callback.message.edit_text(text, reply_markup=back_to_admin_kb())
    await callback.answer()


@router.callback_query(F.data == cb.ADMIN_USERS)
async def cb_admin_users(callback: CallbackQuery) -> None:
    total_user = await count_total_users()
    await callback.message.edit_text(
        f"👥 <b>Total User Terdaftar</b>\n\n{total_user} user",
        reply_markup=back_to_admin_kb(),
    )
    await callback.answer()


@router.callback_query(F.data == cb.ADMIN_SETTINGS)
async def cb_admin_settings(callback: CallbackQuery) -> None:
    await callback.message.edit_text(texts.ADMIN_SETTINGS_TEXT, reply_markup=back_to_admin_kb())
    await callback.answer()


async def _render_orders_page(page: int) -> tuple[str, int]:
    orders, total = await get_orders_page(page=page, per_page=ORDERS_PER_PAGE)
    total_pages = max((total + ORDERS_PER_PAGE - 1) // ORDERS_PER_PAGE, 1)

    if not orders:
        return "📦 Belum ada order masuk.", total_pages

    lines = [f"📦 <b>ORDER MASUK</b> (Halaman {page}/{total_pages})\n"]
    for order in orders:
        lines.append(
            f"🔖 <b>#{order.id}</b> | {safe_html(order.username)} | {safe_html(order.paket)}\n"
            f"Durasi: {safe_html(order.durasi)} | LPM: {safe_html(order.jumlah_lpm)}\n"
            f"Status: {safe_html(order.status)} | {format_datetime(order.created_at)}\n"
        )

    return "\n".join(lines), total_pages


@router.callback_query(F.data == cb.ADMIN_ORDERS)
async def cb_admin_orders(callback: CallbackQuery) -> None:
    text, total_pages = await _render_orders_page(page=1)
    await callback.message.edit_text(text, reply_markup=orders_pagination_kb(1, total_pages))
    await callback.answer()


@router.callback_query(F.data.startswith(cb.ADMIN_ORDERS_PAGE_PREFIX))
async def cb_admin_orders_page(callback: CallbackQuery) -> None:
    page = int(callback.data.replace(cb.ADMIN_ORDERS_PAGE_PREFIX, "", 1))
    text, total_pages = await _render_orders_page(page=page)
    await callback.message.edit_text(text, reply_markup=orders_pagination_kb(page, total_pages))
    await callback.answer()


@router.callback_query(F.data == cb.ADMIN_BROADCAST)
async def cb_admin_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(BroadcastState.waiting_content)
    await callback.message.edit_text(texts.ADMIN_BROADCAST_ASK_CONTENT)
    await callback.answer()


@router.message(BroadcastState.waiting_content)
async def process_broadcast_content(message: Message, state: FSMContext) -> None:
    await state.update_data(source_chat_id=message.chat.id, source_message_id=message.message_id)
    await state.set_state(BroadcastState.confirmation)
    await message.copy_to(chat_id=message.chat.id)
    await message.answer(
        texts.ADMIN_BROADCAST_CONFIRM,
        reply_markup=broadcast_confirmation_kb(),
    )


@router.callback_query(BroadcastState.confirmation, F.data == cb.BROADCAST_CONFIRM)
async def confirm_broadcast(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    source_chat_id = data.get("source_chat_id")
    source_message_id = data.get("source_message_id")

    await callback.answer("Mengirim broadcast, mohon tunggu...")

    try:
        source_message = await bot.forward_message(
            chat_id=source_chat_id,
            from_chat_id=source_chat_id,
            message_id=source_message_id,
            disable_notification=True,
        )
        result = await broadcast_message(bot, source_message)
        await bot.delete_message(chat_id=source_chat_id, message_id=source_message.message_id)
    except Exception:
        logger.exception("Gagal melakukan broadcast.")
        await callback.message.answer("⚠️ Terjadi kesalahan saat mengirim broadcast.")
        await state.clear()
        return

    result_text = texts.ADMIN_BROADCAST_RESULT_TEMPLATE.format(
        total=result.total, success=result.success, failed=result.failed
    )
    await callback.message.edit_text(result_text, reply_markup=back_to_admin_kb())
    await state.clear()


@router.callback_query(BroadcastState.confirmation, F.data == cb.BROADCAST_CANCEL)
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text("❌ Broadcast dibatalkan.", reply_markup=back_to_admin_kb())
    await callback.answer()


ORDER_ID_TELEGRAM_PATTERN = re.compile(r"ID Telegram\s*:\s*(\d+)")


@router.message(F.reply_to_message, ~F.text.startswith("/"))
async def forward_admin_reply_to_customer(message: Message, bot: Bot) -> None:
    """
    Menangani balasan admin terhadap notifikasi order.
    Balasan admin akan otomatis diteruskan ke customer terkait.
    """
    replied_text = message.reply_to_message.text or message.reply_to_message.caption or ""
    match = ORDER_ID_TELEGRAM_PATTERN.search(replied_text)

    if not match:
        # Bukan reply terhadap notifikasi order, abaikan.
        return

    customer_telegram_id = int(match.group(1))

    try:
        await message.copy_to(chat_id=customer_telegram_id)
        await message.answer("✅ Balasan berhasil diteruskan ke customer.")
    except Exception:
        logger.exception("Gagal meneruskan balasan admin ke customer %s", customer_telegram_id)
        await message.answer("⚠️ Gagal meneruskan balasan ke customer. Mungkin bot diblokir.")
