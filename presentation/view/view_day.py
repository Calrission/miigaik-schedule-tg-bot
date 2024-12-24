import dataclasses
import datetime

from common.utils import human_date, human_week_day
from data.models.model_lesson import ModelLesson


@dataclasses.dataclass
class ViewDay:
    index_weekday: int
    name: str
    date: datetime.datetime
    next_date: datetime.datetime
    prev_date: datetime.datetime
    lessons: list[ModelLesson]

    @property
    def str_next_date(self): return human_date(self.next_date)

    @property
    def str_prev_date(self): return human_date(self.prev_date)

    @property
    def str_date(self): return human_date(self.date)

    @property
    def str_weekday(self): return human_week_day(self.index_weekday)

    def __str__(self): return (f"{self.str_weekday} | {self.str_date} | {self.name}\n\n"
                               f"{"\n\n".join(map(str, self.lessons))}")
