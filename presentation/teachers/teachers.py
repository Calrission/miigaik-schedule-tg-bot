from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from domain.schedule_use_case import get_teacher_schedule
from domain.states.teacher_state import TeacherState
from domain.teacher_use_case import search_teacher_by_name
from loader import dp, bot
from presentation import simple_list_keyboard, get_schedule_keyboard
from presentation.view.view_error import ViewError


@dp.message(Command("teacher"))
async def command_teacher(message: Message, state: FSMContext):
    await state.set_state(TeacherState.teacher_name)
    await message.answer("Введите ФИО преподавателя: ")


@dp.message(TeacherState.teacher_name)
async def enter_name_teacher(message: Message, state: FSMContext):
    name = message.text
    view = search_teacher_by_name(name)
    if isinstance(view, ViewError):
        await message.answer(view.error)
        return
    await state.set_state(TeacherState.teacher_choose)
    await state.update_data(teachers=view)

    keyboard = simple_list_keyboard(list(map(str, view)), f"teacher_")
    send_message = await message.answer("Выберите преподавателя или введите еще раз:", reply_markup=keyboard)
    await state.update_data(choose_teacher_message_id=(send_message.chat.id, send_message.message_id))


@dp.message(TeacherState.teacher_choose)
async def reenter_teacher_name(message: Message, state: FSMContext):
    chat_id, message_id = (await state.get_data())["choose_teacher_message_id"]
    await bot.delete_message(chat_id, message_id)
    await enter_name_teacher(message, state)


@dp.callback_query(F.data.startswith("teacher_"), TeacherState.teacher_choose)
async def choose_teacher(callback: CallbackQuery, state: FSMContext):
    await state.set_state(TeacherState.teacher_choose)
    teacher_index = int(callback.data.replace("teacher_", ""))
    teachers = (await state.get_data())["teachers"]
    teacher = teachers[teacher_index]
    await state.update_data(teacher=teacher)
    view = get_teacher_schedule(callback.message.date, teacher)
    if isinstance(view, ViewError):
        await callback.message.answer(view.error)
        return
    keyboard = get_schedule_keyboard(
        view.str_prev_date,
        view.str_date,
        view.str_next_date,
        "teacher"
    )
    await callback.message.answer(str(view), reply_markup=keyboard)
    await callback.message.delete()
