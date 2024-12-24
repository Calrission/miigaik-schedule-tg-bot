from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F
from domain.classroom_use_case import search_classroom
from domain.schedule_use_case import get_classroom_schedule
from domain.states.classroom_state import ClassroomState
from loader import dp, bot
from presentation import simple_list_keyboard, get_schedule_keyboard
from presentation.view.view_error import ViewError


@dp.message(Command("classroom"))
async def command_classroom(message: Message, state: FSMContext):
    await state.set_state(ClassroomState.classroom_name)
    await message.answer("Введите номер аудитории: ")


@dp.message(ClassroomState.classroom_name)
async def enter_classroom_name(message: Message, state: FSMContext):
    classroom_name = message.text
    view = search_classroom(classroom_name)
    if isinstance(view, ViewError):
        await message.answer(view.error)
        return
    if len(view) == 1:
        view = get_classroom_schedule(message.date, view[0])
        if isinstance(view, ViewError):
            await message.answer(view.error)
            return
        keyboard = get_schedule_keyboard(
            view.str_prev_date,
            view.str_date,
            view.str_next_date
        )
        await message.answer(str(view), reply_markup=keyboard)
    await state.set_state(ClassroomState.classroom_choose)
    await state.update_data(classrooms=view)
    keyboard = simple_list_keyboard(list(map(str, view)), f"classroom_")
    send_message = await message.answer("Выберите аудиторию или введите еще раз:", reply_markup=keyboard)
    await state.update_data(choose_message_id=(send_message.chat.id, send_message.message_id))


@dp.message(ClassroomState.classroom_choose)
async def reenter_classroom_name(message: Message, state: FSMContext):
    chat_id, message_id = (await state.get_data())["choose_message_id"]
    await bot.delete_message(chat_id, message_id)
    await enter_classroom_name(message, state)


@dp.callback_query(F.data.startswith("classroom_"), ClassroomState.classroom_choose)
async def choose_classroom(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ClassroomState.classroom_choose)
    classroom_index = int(callback.data.replace("classroom_", ""))
    classrooms = (await state.get_data())["classrooms"]
    classroom = classrooms[classroom_index]
    view = get_classroom_schedule(callback.message.date, classroom)
    if isinstance(view, ViewError):
        await callback.message.answer(view.error)
        return
    keyboard = get_schedule_keyboard(
        view.str_prev_date,
        view.str_date,
        view.str_next_date
    )
    await state.clear()
    await callback.message.answer(str(view), reply_markup=keyboard)
    await callback.message.delete()
