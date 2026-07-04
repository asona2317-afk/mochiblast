"""
FSM state untuk fitur broadcast admin.
"""

from aiogram.fsm.state import State, StatesGroup


class BroadcastState(StatesGroup):
    waiting_content = State()
    confirmation = State()
