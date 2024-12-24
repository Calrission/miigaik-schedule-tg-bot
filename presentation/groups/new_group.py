from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from data.models.model_group import ModelGroup
from domain.states.data_state import DataState
from domain.states.new_group_state import NewGroupState
from domain.states.utils import actualize_state
from loader import api, dp, db
from presentation.keyboards import simple_list_keyboard
from presentation.utils import get_buttons_text_message


@dp.message(Command("new_group"))
async def add_new_group(message: Message, state: FSMContext):
    groups = api.fetch_all_groups()
    await state.set_state(DataState.groups)
    await state.update_data(groups=groups)
    await state.set_state(NewGroupState.year)

    years = sorted(set([str(i.year) for i in groups]))
    keyboard = simple_list_keyboard(years, "year_", use_index=False)

    await message.answer("Выберите год поступления:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("year_"), NewGroupState.year)
async def callback_choose_year(callback: CallbackQuery, state: FSMContext):
    year = int(callback.data.replace("year_", ""))
    groups = (await state.get_data())["groups"]

    await state.update_data(year=year)
    await state.set_state(NewGroupState.faculty)

    faculties = sorted(set([i.faculty for i in groups]))
    keyboard = simple_list_keyboard(faculties, "faculty_")

    await callback.message.edit_text("Выберите факультет:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("faculty_"), NewGroupState.faculty)
async def callback_choose_faculty(callback: CallbackQuery, state: FSMContext):
    index_button = int(callback.data.replace("faculty_", ""))
    faculty = get_buttons_text_message(callback.message)[index_button]

    groups: list[ModelGroup] = (await state.get_data())["groups"]
    year = int((await state.get_data())["year"])

    await state.update_data(faculty=faculty)
    await state.set_state(NewGroupState.name_group)

    groups_items = sorted(set([i.group for i in groups if i.faculty == faculty and i.year == year]))
    keyboard = simple_list_keyboard(groups_items, "group_")

    await callback.message.edit_text("Выберите группу:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("group_"), NewGroupState.name_group)
async def callback_choose_group(callback: CallbackQuery, state: FSMContext):
    index_button = int(callback.data.replace("group_", ""))
    group = get_buttons_text_message(callback.message)[index_button]
    groups: list[ModelGroup] = (await state.get_data())["groups"]

    year, faculty, _, _ = await NewGroupState.get_group_name(state)

    subgroups = sorted(
        set([i.subgroup for i in groups if i.group == group and i.year == year and i.faculty == faculty])
    )

    await state.update_data(name_group=group)
    await state.set_state(NewGroupState.sub_group)

    keyboard = simple_list_keyboard(subgroups, "subgroup_")

    await callback.message.edit_text("Выберите подгруппу:", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("subgroup_"), NewGroupState.sub_group)
async def callback_choose_subgroup(callback: CallbackQuery, state: FSMContext):
    index_button = int(callback.data.replace("subgroup_", ""))
    subgroup = get_buttons_text_message(callback.message)[index_button]
    groups: list[ModelGroup] = (await state.get_data())["groups"]
    already_have_groups = [i.name for i in db.fetch_user_groups(callback.from_user.id)]

    year, faculty, group, _ = await NewGroupState.get_group_name(state)

    groups = [i for i in groups if i == (year, faculty, group, subgroup)]

    if len(groups) != 1:
        await callback.answer("Что-то пошло не так, группа не найдена")
        return

    if groups[0].name in already_have_groups:
        await callback.answer("Вы уже добавили эту группу ранее")
        await actualize_state(callback.from_user.id, state)
    else:
        model_group = groups[0]

        await state.update_data(subgroup=subgroup)
        await state.set_state(DataState.group)
        await state.update_data(group=model_group)

        db.insert_group(model_group.id, model_group.name, callback.from_user.id, True)

    await callback.message.edit_text(
        "Введите /schedule для получения расписания\nВведите /groups чтобы выбрать группу",
        reply_markup=None
    )
