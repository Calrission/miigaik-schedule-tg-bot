import dataclasses
from typing import Any
from data.models.model_schedule import ModelSchedule


@dataclasses.dataclass
class ModelScheduleGroup:
    group_name: str
    schedule: ModelSchedule

    @staticmethod
    def from_json(json: dict[str, Any]) -> 'ModelScheduleGroup':
        return ModelScheduleGroup(
            group_name=json['groupName'],
            schedule=ModelSchedule.from_json(json['schedule']),
        )
