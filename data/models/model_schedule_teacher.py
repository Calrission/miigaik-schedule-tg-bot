import dataclasses

from data.models.model_schedule import ModelSchedule
from data.models.model_teacher import ModelTeacher


@dataclasses.dataclass
class ModelScheduleTeacher:
    teacher: ModelTeacher
    schedule: ModelSchedule

    @staticmethod
    def from_json(json: dict) -> 'ModelScheduleTeacher':
        return ModelScheduleTeacher(
            teacher=ModelTeacher.from_json(json['teacher']),
            schedule=ModelSchedule.from_json(json['schedule']),
        )
