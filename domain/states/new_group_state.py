from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


class NewGroupState(StatesGroup):
    year = State()
    faculty = State()
    name_group = State()
    sub_group = State()

    @staticmethod
    async def all(context: FSMContext) -> (int | None, str | None, str | None, str | None):
        state_data = await context.get_data()

        def safe_get(key: str):
            return state_data[key] if key in state_data else None

        year = int(safe_get("year"))
        faculty = safe_get("faculty")
        group = safe_get("name_group")
        subgroup = safe_get("subgroup")

        return year, faculty, group, subgroup
