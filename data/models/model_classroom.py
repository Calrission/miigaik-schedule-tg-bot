import dataclasses


@dataclasses.dataclass
class ModelClassroom:
    id: int
    name: str

    @staticmethod
    def from_json(json: dict) -> 'ModelClassroom':
        return ModelClassroom(
            id=json['classroomId'],
            name=json['classroomName'],
        )

    def __str__(self) -> str:
        return self.name
