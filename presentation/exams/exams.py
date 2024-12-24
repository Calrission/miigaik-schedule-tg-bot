from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from data.models.model_group import ModelGroup
from domain.exams import get_exams
from domain.states.data_state import DataState
from domain.states.utils import actualize_state
from loader import dp
from presentation import add_new_group


@dp.message(Command("exams"), DataState.group)
async def command_exam(message: Message, state: FSMContext):
    await actualize_state(message.from_user.id, state)
    group: ModelGroup = (await state.get_data())["group"]
    message_text = get_exams(group)
    await message.answer(message_text)


@dp.message(Command("exams"))
async def command_exam_not_select_group(message: Message, state: FSMContext):
    await actualize_state(message.from_user.id, state)
    if (await state.get_state()) == DataState.group:
        await command_exam(message, state)
    else:
        await add_new_group(message, state)
