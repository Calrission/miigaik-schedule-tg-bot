import dataclasses
from datetime import datetime
from typing import Any

from data.models.model_teacher import ModelTeacher


@dataclasses.dataclass
class ModelLesson:
    day_of_week: str
    group_name: str
    lesson_date: datetime
    lesson_order_number: int
    lesson_start_time: str
    lesson_end_time: str
    lesson_type: str
    classroom_name: str
    classroom_floor: int
    classroom_building: str
    discipline_name: str
    teachers: list[ModelTeacher]

    @staticmethod
    def from_json(json: dict[str, Any], day_of_week: str) -> 'ModelLesson':
        return ModelLesson(
            day_of_week=day_of_week,
            group_name=json['groupName'],
            lesson_date=datetime.fromisoformat(json["lessonDate"]),
            lesson_order_number=int(json["lessonOrderNumber"]),
            lesson_start_time=":".join(str(json["lessonStartTime"]).split(":")[:2]),
            lesson_end_time=":".join(str(json["lessonEndTime"]).split(":")[:2]),
            lesson_type=json["lessonType"],
            classroom_name=json["classroomName"],
            classroom_floor=int(json["classroomFloor"]),
            classroom_building=json["classroomBuilding"],
            discipline_name=json["disciplineName"],
            teachers=[ModelTeacher.from_json(i) for i in json["teachers"]]
        )