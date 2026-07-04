"""
FSM state untuk alur pemesanan (order).
"""

from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    waiting_username = State()
    waiting_teks_sebar = State()
    waiting_durasi = State()
    waiting_jumlah_lpm = State()
    waiting_request_lpm = State()
    confirmation = State()
