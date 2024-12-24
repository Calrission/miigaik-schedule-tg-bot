from aiogram.fsm.state import StatesGroup, State


class DataState(StatesGroup):
    groups = State()
    group = State()
