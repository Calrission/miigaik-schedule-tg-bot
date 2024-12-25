from datetime import datetime, timedelta

from aiogram.fsm.context import FSMContext

from data.models.model_classroom import ModelClassroom
from data.models.model_group import ModelGroup
from data.models.model_schedule_classroom import ModelScheduleClassroom
from data.models.model_schedule_group import ModelScheduleGroup
from data.models.model_schedule_teacher import ModelScheduleTeacher
from data.models.model_search_teacher import ModelSearchTeacher
from data.models.model_teacher import ModelTeacher
from domain.utils import date_unix
from loader import api
from presentation.view.view_day import ViewDay
from presentation.view.view_error import ViewError


def get_group_schedule(date: datetime, group: ModelGroup) -> ViewDay | ViewError:
    day_of_week = date.weekday()
    link = group.calc_link_group(date_unix(date))
    try:
        response: ModelScheduleGroup = api.fetch_schedule_group(link)
        lessons = response.schedule.from_index(day_of_week)
        next_date = date + timedelta(days=1)
        prev_date = date - timedelta(days=1)
        return ViewDay(
            index_weekday=day_of_week,
            lessons=lessons,
            next_date=next_date,
            prev_date=prev_date,
            date=date,
            name=group.name
        )
    except Exception as e:
        return ViewError.something_went_wrong(e)


def get_classroom_schedule(date: datetime, classroom: ModelClassroom) -> ViewDay | ViewError:
    day_of_week = date.weekday()
    try:
        response: ModelScheduleClassroom = api.fetch_schedule_classroom(classroom.current_week_schedule_link)
        lessons = response.schedule.from_index(day_of_week)
        next_date = date + timedelta(days=1)
        prev_date = date - timedelta(days=1)
        return ViewDay(
            index_weekday=day_of_week,
            lessons=lessons,
            next_date=next_date,
            prev_date=prev_date,
            date=date,
            name=classroom.name
        )
    except Exception as e:
        return ViewError.something_went_wrong(e)


def get_teacher_schedule(date: datetime, teacher: ModelSearchTeacher) -> ViewDay | ViewError:
    day_of_week = date.weekday()
    try:
        response: ModelScheduleTeacher = api.fetch_schedule_teacher(teacher.current_week_schedule_link)
        lessons = response.schedule.from_index(day_of_week)
        next_date = date + timedelta(days=1)
        prev_date = date - timedelta(days=1)
        return ViewDay(
            index_weekday=day_of_week,
            lessons=lessons,
            next_date=next_date,
            prev_date=prev_date,
            date=date,
            name=str(teacher.teacher)
        )
    except Exception as e:
        import traceback
        return ViewError.something_went_wrong(e)


async def change_schedule(str_date: str, postfix: str, state: FSMContext) -> ViewDay | ViewError:
    date = datetime.strptime(str_date, "%d.%m.%Y")

    if postfix == "group":
        group = (await state.get_data())["group"]
        view = get_group_schedule(date, group)
    elif postfix == "classroom":
        classroom = (await state.get_data())["classroom"]
        view = get_classroom_schedule(date, classroom)
    elif postfix == "teacher":
        teacher = (await state.get_data())["teacher"]
        view = get_teacher_schedule(date, teacher)
    else:
        view = ViewError(error="Неизвестный postfix")
    return view
