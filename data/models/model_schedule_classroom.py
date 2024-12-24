import dataclasses
from typing import Any
from data.models.model_schedule import ModelSchedule


@dataclasses.dataclass
class ModelScheduleClassroom:
    classroom_name: str
    schedule: ModelSchedule

    @staticmethod
    def from_json(json: dict[str, Any]) -> 'ModelScheduleClassroom':
        return ModelScheduleClassroom(
            classroom_name=json['classroomName'],
            schedule=ModelSchedule.from_json(json['schedule']),
        )
