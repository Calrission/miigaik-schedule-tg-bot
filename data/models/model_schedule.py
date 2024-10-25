from dataclasses import dataclass
from typing import Optional

from data.models.model_lesson import ModelLesson


@dataclass
class ModelSchedule:
    monday: Optional[list[ModelLesson]]
    tuesday: Optional[list[ModelLesson]]
    wednesday: Optional[list[ModelLesson]]
    thursday: Optional[list[ModelLesson]]
    friday: Optional[list[ModelLesson]]
    saturday: Optional[list[ModelLesson]]
    sunday: Optional[list[ModelLesson]]

    @staticmethod
    def from_json(json: dict[str, list]) -> 'ModelSchedule':
        def convert(day_of_week: str) -> list[ModelLesson]:
            if day_of_week not in json:
                return []
            value = json[day_of_week]
            return [ModelLesson.from_json(i, day_of_week) for i in value]

        return ModelSchedule(
            monday=convert("понедельник"),
            tuesday=convert("вторник"),
            wednesday=convert("среда"),
            thursday=convert("четверг"),
            friday=convert("пятница"),
            saturday=convert("суббота"),
            sunday=convert("воскресенье"),
        )

    def from_index(self, index: int) -> list[ModelLesson]:
        return [self.monday, self.tuesday, self.wednesday, self.thursday, self.friday, self.saturday, self.sunday][index]

