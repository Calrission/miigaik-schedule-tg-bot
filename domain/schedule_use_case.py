from datetime import datetime, timedelta

from data.models.model_classroom import ModelClassroom
from data.models.model_group import ModelGroup
from data.models.model_schedule_classroom import ModelScheduleClassroom
from data.models.model_schedule_group import ModelScheduleGroup
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
        import traceback
        print(traceback.format_exc())
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
        import traceback
        print(traceback.format_exc())
        return ViewError.something_went_wrong(e)
