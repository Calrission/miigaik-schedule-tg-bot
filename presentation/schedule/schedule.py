from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from domain.schedule import get_schedule
from domain.states.data_state import DataState
from loader import dp
from main import actualize_state
from presentation import add_new_group
from presentation.keyboards import get_schedule_keyboard


@dp.message(Command("schedule"), DataState.group)
async def command_schedule(message: Message, state: FSMContext) -> None:
    await actualize_state(message.from_user.id, state)
    group = (await state.get_data())["group"]
    message_text, prev_date, now_date, next_date = get_schedule(message.date, group)
    keyboard = get_schedule_keyboard(prev_date, now_date, next_date)
    await message.answer(message_text, reply_markup=keyboard)


@dp.callback_query(F.data.startswith("change_"), DataState.group)
async def next_prev_schedule_handler(callback: CallbackQuery, state: FSMContext) -> None:
    str_date = callback.data.replace("change_", "")
    group = (await state.get_data())["group"]
    message_text, prev_date, now_date, next_date = get_schedule(str_date, group)
    keyboard = get_schedule_keyboard(prev_date, now_date, next_date)
    await callback.message.edit_text(message_text, reply_markup=keyboard)


@dp.message(Command("schedule"))
async def command_schedule_not_select_group(message: Message, state: FSMContext) -> None:
    await actualize_state(message.from_user.id, state)
    if (await state.get_state()) == DataState.group:
        await command_schedule(message, state)
    else:
        await add_new_group(message, state)
