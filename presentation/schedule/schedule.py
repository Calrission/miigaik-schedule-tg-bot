from datetime import datetime
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from domain.schedule_use_case import get_group_schedule, get_classroom_schedule, change_schedule
from domain.states.data_state import DataState
from loader import dp
from main import actualize_state
from presentation import add_new_group
from presentation.keyboards import get_schedule_keyboard
from presentation.view.view_error import ViewError


@dp.message(Command("schedule"), DataState.group)
async def command_schedule(message: Message, state: FSMContext) -> None:
    await actualize_state(message.from_user.id, state)
    group = (await state.get_data())["group"]
    view = get_group_schedule(message.date, group)
    if isinstance(view, ViewError):
        await message.answer(view.error)
        return
    keyboard = get_schedule_keyboard(
        view.str_prev_date,
        view.str_date,
        view.str_next_date,
        "group"
    )
    await message.answer(str(view), reply_markup=keyboard)


@dp.callback_query(F.data.startswith("change_"))
async def next_prev_schedule_handler(callback: CallbackQuery, state: FSMContext) -> None:
    str_date, postfix = callback.data.replace("change_", "").split("_")

    view = await change_schedule(str_date, postfix, state)

    if isinstance(view, ViewError):
        await callback.message.answer(view.error)
        return

    keyboard = get_schedule_keyboard(
        view.str_prev_date,
        view.str_date,
        view.str_next_date,
        postfix
    )
    await callback.message.edit_text(str(view), reply_markup=keyboard)


@dp.message(Command("schedule"))
async def command_schedule_not_select_group(message: Message, state: FSMContext) -> None:
    await actualize_state(message.from_user.id, state)
    if (await state.get_state()) == DataState.group:
        await command_schedule(message, state)
    else:
        await add_new_group(message, state)
