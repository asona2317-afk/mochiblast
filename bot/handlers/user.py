"""
Handler untuk menu-menu customer: /start, Pricelist, Cara Order,
Keunggulan, Admin, dan Channel.
"""

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.keyboards import callback_data as cb
from bot.keyboards.user import (
    admin_contact_kb,
    back_to_main_kb,
    channel_kb,
    main_menu_kb,
    package_detail_kb,
    pricelist_kb,
)
from bot.utils import texts
from bot.utils.logger import get_logger

router = Router(name="user_router")
logger = get_logger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(texts.WELCOME_TEXT, reply_markup=main_menu_kb())


@router.callback_query(F.data == cb.MENU_MAIN)
async def cb_main_menu(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(texts.WELCOME_TEXT, reply_markup=main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == cb.MENU_PRICELIST)
async def cb_pricelist(callback: CallbackQuery) -> None:
    await callback.message.edit_text(texts.PRICELIST_TITLE, reply_markup=pricelist_kb())
    await callback.answer()


@router.callback_query(F.data == cb.PRICELIST_BASIC)
async def cb_pricelist_basic(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        texts.MOCHI_BASIC_TEXT, reply_markup=package_detail_kb("basic")
    )
    await callback.answer()


@router.callback_query(F.data == cb.PRICELIST_PREMIUM)
async def cb_pricelist_premium(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        texts.MOCHI_PREMIUM_TEXT, reply_markup=package_detail_kb("premium")
    )
    await callback.answer()


@router.callback_query(F.data == cb.MENU_CARA_ORDER)
async def cb_cara_order(callback: CallbackQuery) -> None:
    await callback.message.edit_text(texts.CARA_ORDER_TEXT, reply_markup=back_to_main_kb())
    await callback.answer()


@router.callback_query(F.data == cb.MENU_KEUNGGULAN)
async def cb_keunggulan(callback: CallbackQuery) -> None:
    await callback.message.edit_text(texts.KEUNGGULAN_TEXT, reply_markup=back_to_main_kb())
    await callback.answer()


@router.callback_query(F.data == cb.MENU_ADMIN)
async def cb_admin_info(callback: CallbackQuery) -> None:
    text = texts.ADMIN_INFO_TEXT.format(admin_username=settings.admin_username)
    await callback.message.edit_text(text, reply_markup=admin_contact_kb())
    await callback.answer()


@router.callback_query(F.data == cb.MENU_CHANNEL)
async def cb_channel_info(callback: CallbackQuery) -> None:
    text = texts.CHANNEL_INFO_TEXT.format(channel_username=settings.channel_username)
    await callback.message.edit_text(text, reply_markup=channel_kb())
    await callback.answer()
