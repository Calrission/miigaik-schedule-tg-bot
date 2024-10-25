from aiogram.types import InlineKeyboardMarkup

from loader import db
from presentation.keyboards import get_favorite_inline_keyboard


def get_command_groups(id_user: int):
    groups = db.fetch_user_groups(id_user)
    favorite_group_id = db.fetch_favorite_user_group(id_user).id
    keyboard = get_favorite_inline_keyboard(groups, favorite_group_id)
    return "Выберите избранную группу:", keyboard


def change_favorite(new_favorite_group_id: int, user_id: int) -> (str, InlineKeyboardMarkup):
    now_favorite_group_id = db.fetch_favorite_user_group(user_id).id
    if now_favorite_group_id == new_favorite_group_id:
        return "Группа уже выбрана"
    db.set_favorite_group(user_id, new_favorite_group_id)
    groups = db.fetch_user_groups(user_id)
    keyboard = get_favorite_inline_keyboard(groups, new_favorite_group_id)
    return keyboard
