from aiogram.fsm.context import FSMContext

from domain.states.data_state import DataState
from loader import db


async def actualize_state(user_id: int, state: FSMContext):
    group = db.fetch_favorite_user_group(user_id=user_id)
    if group is not None:
        await state.update_data(group=group)
        await state.set_state(DataState.group)
