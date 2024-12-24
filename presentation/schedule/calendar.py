from datetime import datetime
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from domain.schedule_use_case import get_group_schedule
from domain.states.data_state import DataState
from domain.states.utils import actualize_state
from loader import dp
from presentation.keyboards import get_calendar_keyboard, get_schedule_keyboard
from presentation.view.view_error import ViewError


@dp.callback_query(F.data.startswith("calendar_change_"))
async def calendar_change(callback: CallbackQuery):
    new_date_str = callback.data.replace("calendar_change_", "")
    date = datetime.strptime(new_date_str, "%d.%m.%Y")
    new_keyboard = get_calendar_keyboard(date)
    await callback.message.edit_reply_markup(reply_markup=new_keyboard)


@dp.callback_query(F.data.startswith("day_"))
async def select_day_calendar_handler(callback: CallbackQuery, state: FSMContext):
    await actualize_state(callback.from_user.id, state)
    date_str = callback.data.replace("day_", "")
    date = datetime.strptime(date_str, "%d.%m.%Y")
    group = (await state.get_data())["group"]
    view = get_group_schedule(date, group)
    if isinstance(view, ViewError):
        await callback.message.answer(view.error)
        return
    keyboard = get_schedule_keyboard(
        view.str_prev_date,
        view.str_date,
        view.str_next_date
    )
    await callback.message.edit_text(str(view), reply_markup=keyboard)


@dp.callback_query(F.data.startswith("calendar_"), DataState.group)
async def calendar_schedule_handler(callback: CallbackQuery) -> None:
    selected_date_str = callback.data.replace("calendar_", "")
    date = datetime.strptime(selected_date_str, "%d.%m.%Y")
    keyboard = get_calendar_keyboard(date)
    await callback.message.edit_text("Выберите дату: ", reply_markup=keyboard)
