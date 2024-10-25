from datetime import datetime, timedelta

from common.utils import human_date, human_week_day
from data.models.model_group import ModelGroup
from data.models.model_lesson import ModelLesson
from data.models.model_schedule_group import ModelScheduleGroup
from loader import api


def get_schedule(date: datetime | str, group: ModelGroup) -> (str, str, str, str):
    if isinstance(date, datetime):
        str_date = human_date(date)
    else:
        str_date = date[:]
        date = datetime.strptime(date, "%d.%m.%Y")
    day_of_week = date.weekday()
    date_unix = int((date - datetime(1970, 1, 1, tzinfo=date.tzinfo)).total_seconds())

    link = group.calc_link(date_unix)
    response: ModelScheduleGroup = api.fetch_schedule(link)
    lessons = response.schedule.from_index(day_of_week)

    def lessons_block(lst: list[ModelLesson]) -> str:
        return "\n\n".join([
            f"{i.lesson_order_number} пара {i.lesson_start_time} - {i.lesson_end_time}\n"
            f"{i.discipline_name}\n"
            f"{", ".join([str(j) for j in i.teachers])}\n"
            f"{i.lesson_type}\n"
            f"{'Аудитория ' if i.classroom_name != 'Военный учебный центр' else ''}{i.classroom_name} | {i.classroom_building} | {i.classroom_floor} этаж"
            for i in lst
        ])

    message_text = (f"{human_week_day(day_of_week)} | {human_date(date)}\n\n"
                    f"{lessons_block(lessons)}")

    str_next_date = human_date(date + timedelta(days=1))
    str_prev_date = human_date(date - timedelta(days=1))

    return message_text, str_prev_date, str_date, str_next_date
