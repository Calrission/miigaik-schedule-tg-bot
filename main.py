from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from domain.states.utils import actualize_state
from loader import *
import presentation


@dp.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext) -> None:
    await actualize_state(message.from_user.id, state)
    current_state = await state.get_data()

    if current_state == {}:
        await presentation.groups.add_new_group(message, state)
    else:
        await presentation.schedule.command_schedule(message, state)
