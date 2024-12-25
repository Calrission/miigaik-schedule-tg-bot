from aiogram.fsm.state import StatesGroup, State


class ClassroomState(StatesGroup):
    classroom_name = State()
    classroom_choose = State()
