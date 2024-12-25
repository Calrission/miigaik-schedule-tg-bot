import dataclasses

from data.models.model_teacher import ModelTeacher


@dataclasses.dataclass
class ModelSearchTeacher:
    id: int
    teacher: ModelTeacher
    current_week_schedule_link: str

    @staticmethod
    def from_json(data: dict) -> 'ModelSearchTeacher':
        return ModelSearchTeacher(
            id=data['id'],
            teacher=ModelTeacher.from_json(data['teacher']),
            current_week_schedule_link=data['currentWeekScheduleLink'],
        )

    def __str__(self) -> str:
        return str(self.teacher)

