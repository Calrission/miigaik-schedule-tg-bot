import dataclasses


@dataclasses.dataclass
class ModelClassroom:
    id: int
    name: str
    current_week_schedule_link: str

    @staticmethod
    def from_json(json: dict) -> 'ModelClassroom':
        return ModelClassroom(
            id=json['classroomId'],
            name=json['classroomName'],
            current_week_schedule_link=json['currentWeekScheduleLink']
        )

    def __str__(self) -> str:
        return self.name
