"""
Handler untuk alur pemesanan (order) menggunakan FSM.
"""

from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.keyboards import callback_data as cb
from bot.keyboards.user import (
    confirmation_kb,
    durasi_kb,
    jumlah_lpm_kb,
    main_menu_kb,
    skip_request_kb,
)
from bot.services.order_service import create_order
from bot.states.order import OrderState
from bot.utils import texts
from bot.utils.logger import get_logger
from bot.utils.text import safe_html

router = Router(name="order_router")
logger = get_logger(__name__)

PAKET_LABEL = {
    "basic": "Mochi Basic",
    "premium": "Mochi Premium",
}


@router.callback_query(F.data == cb.ORDER_START_BASIC)
async def start_order_basic(callback: CallbackQuery, state: FSMContext) -> None:
    await _start_order(callback, state, paket="basic")


@router.callback_query(F.data == cb.ORDER_START_PREMIUM)
async def start_order_premium(callback: CallbackQuery, state: FSMContext) -> None:
    await _start_order(callback, state, paket="premium")


async def _start_order(callback: CallbackQuery, state: FSMContext, paket: str) -> None:
    await state.set_state(OrderState.waiting_username)
    await state.update_data(paket=paket)
    await callback.message.edit_text(texts.ORDER_ASK_USERNAME)
    await callback.answer()


@router.message(OrderState.waiting_username)
async def process_username(message: Message, state: FSMContext) -> None:
    username = (message.text or "").strip()
    if not username:
        await message.answer("⚠️ Username tidak boleh kosong. Silakan kirim ulang.")
        return

    await state.update_data(order_username=username)
    await state.set_state(OrderState.waiting_teks_sebar)
    await message.answer(texts.ORDER_ASK_TEKS_SEBAR)


@router.message(OrderState.waiting_teks_sebar)
async def process_teks_sebar(message: Message, state: FSMContext) -> None:
    teks_sebar = (message.text or message.caption or "").strip()
    if not teks_sebar:
        await message.answer("⚠️ Teks sebar tidak boleh kosong. Silakan kirim ulang.")
        return

    await state.update_data(teks_sebar=teks_sebar)
    await state.set_state(OrderState.waiting_durasi)
    await message.answer(texts.ORDER_ASK_DURASI, reply_markup=durasi_kb())


@router.callback_query(OrderState.waiting_durasi, F.data.startswith(cb.ORDER_DURASI_PREFIX))
async def process_durasi(callback: CallbackQuery, state: FSMContext) -> None:
    durasi = callback.data.replace(cb.ORDER_DURASI_PREFIX, "", 1)
    await state.update_data(durasi=durasi)
    await state.set_state(OrderState.waiting_jumlah_lpm)
    await callback.message.edit_text(texts.ORDER_ASK_JUMLAH_LPM, reply_markup=jumlah_lpm_kb())
    await callback.answer()


@router.callback_query(OrderState.waiting_jumlah_lpm, F.data.startswith(cb.ORDER_LPM_PREFIX))
async def process_jumlah_lpm(callback: CallbackQuery, state: FSMContext) -> None:
    jumlah_lpm = callback.data.replace(cb.ORDER_LPM_PREFIX, "", 1)
    await state.update_data(jumlah_lpm=jumlah_lpm)
    await state.set_state(OrderState.waiting_request_lpm)
    await callback.message.edit_text(texts.ORDER_ASK_REQUEST_LPM, reply_markup=skip_request_kb())
    await callback.answer()


@router.callback_query(OrderState.waiting_request_lpm, F.data == cb.ORDER_SKIP_REQUEST)
async def skip_request_lpm(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(request_lpm="-")
    await _show_summary(callback.message, state, edit=True)
    await callback.answer()


@router.message(OrderState.waiting_request_lpm)
async def process_request_lpm(message: Message, state: FSMContext) -> None:
    request_lpm = (message.text or message.caption or "-").strip() or "-"
    await state.update_data(request_lpm=request_lpm)
    await _show_summary(message, state, edit=False)


async def _show_summary(message: Message, state: FSMContext, edit: bool) -> None:
    data = await state.get_data()
    await state.set_state(OrderState.confirmation)

    summary_text = texts.ORDER_SUMMARY_TEMPLATE.format(
        username=safe_html(data.get("order_username")),
        paket=PAKET_LABEL.get(data.get("paket"), data.get("paket")),
        durasi=safe_html(data.get("durasi")),
        jumlah_lpm=safe_html(data.get("jumlah_lpm")),
        request_lpm=safe_html(data.get("request_lpm")),
        teks_sebar=safe_html(data.get("teks_sebar")),
    )

    if edit:
        await message.edit_text(summary_text, reply_markup=confirmation_kb())
    else:
        await message.answer(summary_text, reply_markup=confirmation_kb())


@router.callback_query(OrderState.confirmation, F.data == cb.ORDER_CONFIRM)
async def confirm_order(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    data = await state.get_data()
    tg_user = callback.from_user

    order = await create_order(
        telegram_id=tg_user.id,
        username=tg_user.username,
        paket=PAKET_LABEL.get(data.get("paket"), data.get("paket")),
        durasi=data.get("durasi"),
        jumlah_lpm=data.get("jumlah_lpm"),
        request_lpm=data.get("request_lpm"),
        teks_sebar=data.get("teks_sebar"),
    )

    admin_text = texts.ADMIN_NEW_ORDER_TEMPLATE.format(
        nama=safe_html(tg_user.full_name),
        username=safe_html(data.get("order_username")),
        telegram_id=tg_user.id,
        paket=PAKET_LABEL.get(data.get("paket"), data.get("paket")),
        durasi=safe_html(data.get("durasi")),
        jumlah_lpm=safe_html(data.get("jumlah_lpm")),
        request_lpm=safe_html(data.get("request_lpm")),
        teks_sebar=safe_html(data.get("teks_sebar")),
        waktu=datetime.now().strftime("%d-%m-%Y %H:%M"),
    )

    for admin_id in settings.admin_ids:
        try:
            await bot.send_message(chat_id=admin_id, text=admin_text)
        except Exception:
            logger.exception("Gagal mengirim notifikasi order ke admin_id=%s", admin_id)

    await callback.message.edit_text(texts.ORDER_SENT_TO_CUSTOMER, reply_markup=main_menu_kb())
    await callback.answer("Order berhasil dikirim!")
    await state.clear()

    logger.info("Order id=%s berhasil dikonfirmasi oleh telegram_id=%s", order.id, tg_user.id)


@router.callback_query(F.data == cb.ORDER_CANCEL)
async def cancel_order(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(texts.ORDER_CANCELLED_TEXT, reply_markup=main_menu_kb())
    await callback.answer()
