from aiogram.fsm.state import StatesGroup, State


class ClassroomState(StatesGroup):
    # /classrooms -> state = classroom_name -> вводит кабинет -> список найденных кабинет ->
    # state = classroom_choose -> показ списка кабинетов -> выбор кабинета -> запрос расписания ->
    # state.clear() -> показ расписания
    classroom_name = State()
    classroom_choose = State()
