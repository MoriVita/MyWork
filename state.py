from aiogram.fsm.state import State, StatesGroup


class Reg (StatesGroup):
    month = State()
    day = State()
