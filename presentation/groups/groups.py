from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup

from domain.groups import get_command_groups, change_favorite
from loader import dp
from presentation.groups.new_group import add_new_group


@dp.message(Command("groups"))
async def command_groups_handler(message: Message) -> None:
    id_user = message.from_user.id
    message, keyboard = get_command_groups(id_user)
    await message.answer(message, reply_markup=keyboard)


@dp.callback_query(F.data.startswith("favorite_"))
async def change_favorite_handler(callback: CallbackQuery) -> None:
    new_favorite_group_id = int(callback.data.replace("favorite_", ""))
    user_id = callback.from_user.id
    res = change_favorite(new_favorite_group_id, user_id)

    if isinstance(res, InlineKeyboardMarkup):
        await callback.message.edit_reply_markup(reply_markup=res)
    elif isinstance(res, str):
        await callback.answer(res)


@dp.callback_query(F.data == "new_group")
async def new_group_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await add_new_group(callback.message, state)
    await callback.message.delete()
