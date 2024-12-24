import datetime
import calendar

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from common.utils import human_date
from data.models.model_group import ModelGroup


def get_years_inline_keyboard(years: list[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for year in years:
        builder.add(InlineKeyboardButton(text=str(year), callback_data=f"year_{year}"))
    builder.adjust(1)
    return builder.as_markup()


def get_faculty_inline_keyboard(faculties: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, faculty in enumerate(faculties):
        callback_data = f"faculty_{index}"
        builder.add(InlineKeyboardButton(text=faculty, callback_data=callback_data))
    builder.adjust(1)
    return builder.as_markup()


def simple_list_keyboard(lst: list[str], callback_data_prefix: str, use_index: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for index, obj in enumerate(lst):
        callback_data = f"{callback_data_prefix}{index if use_index else obj}"
        builder.add(InlineKeyboardButton(text=obj, callback_data=callback_data))
    builder.adjust(1)
    return builder.as_markup()


def get_schedule_keyboard(prev_date: str, now_date: str, next_date: str) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="⏮️", callback_data=f"change_{prev_date}"),
            InlineKeyboardButton(text="📅", callback_data=f"calendar_{now_date}"),
            InlineKeyboardButton(text="⏭️", callback_data=f"change_{next_date}")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=kb)
    return keyboard


def get_calendar_keyboard(date: datetime.datetime) -> InlineKeyboardMarkup:
    postfix = date.strftime("%m.%Y")

    def placeholder() -> InlineKeyboardButton:
        return InlineKeyboardButton(text=" ", callback_data="placeholder")

    def day(num: int) -> InlineKeyboardButton:
        return InlineKeyboardButton(text=str(num), callback_data=f"day_{num}.{postfix}")

    count_day_in_month = calendar.monthrange(date.year, date.month)[1]
    weekday_first_day_in_month = date.replace(day=1).weekday()
    weekday_last_day_in_month = date.replace(day=count_day_in_month).weekday()
    count_placeholder = count_day_in_month + weekday_first_day_in_month + (7 - weekday_last_day_in_month - 1)
    count_lines = count_placeholder // 7

    placeholder = placeholder()
    lines = []

    prev_date = date - datetime.timedelta(days=date.day)
    next_date = date + datetime.timedelta(days=count_day_in_month - date.day + 1)
    now_month_str = date.strftime("%B")
    now_year_str = date.strftime("%Y")

    lines.append([
        InlineKeyboardButton(text="⏮️", callback_data=f"calendar_change_{human_date(prev_date)}"),
        InlineKeyboardButton(text=now_month_str, callback_data=f"no"),
        InlineKeyboardButton(text=now_year_str, callback_data=f"no"),
        InlineKeyboardButton(text="⏭️", callback_data=f"calendar_change_{human_date(next_date)}"),
    ])

    lines.append([
        InlineKeyboardButton(text="пн", callback_data="no"),
        InlineKeyboardButton(text="вт", callback_data="no"),
        InlineKeyboardButton(text="ср", callback_data="no"),
        InlineKeyboardButton(text="чт", callback_data="no"),
        InlineKeyboardButton(text="пт", callback_data="no"),
        InlineKeyboardButton(text="сб", callback_data="no"),
        InlineKeyboardButton(text="вс", callback_data="no")
    ])

    for i in range(count_lines):
        line = []
        for j in range(7):
            index = i * 7 + j
            if index < weekday_first_day_in_month:
                line.append(placeholder)
            elif index > count_day_in_month + weekday_first_day_in_month - 1:
                line.append(placeholder)
            else:
                line.append(day(index - weekday_first_day_in_month + 1))
        lines.append(line)

    return InlineKeyboardMarkup(inline_keyboard=lines)


def get_favorite_inline_keyboard(groups: list[ModelGroup], favorite_id: int) -> InlineKeyboardMarkup:
    buttons = []
    for group in groups:
        line_button = []
        if favorite_id == group.id:
            line_button.append(InlineKeyboardButton(
                text="⭐",
                callback_data=f"favorite_{group.id}"
            ))
        else:
            line_button.append(InlineKeyboardButton(
                text="🗑️",
                callback_data=f"delete_{group.id}"
            ))
        line_button.append(InlineKeyboardButton(text=group.name, callback_data=f"favorite_{group.id}"))
        buttons.append(line_button)
    buttons.append([InlineKeyboardButton(text="Добавить новую группу", callback_data="new_group")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
