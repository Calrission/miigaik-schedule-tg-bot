from aiogram.fsm.state import StatesGroup, State


class TeacherState(StatesGroup):
    teacher_name = State()
    teacher_choose = State()
