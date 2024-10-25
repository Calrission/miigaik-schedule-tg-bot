import dataclasses


@dataclasses.dataclass
class ModelClassroom:
    class_name: str
    id: int

    @staticmethod
    def from_json(json: dict) -> 'ModelClassroom':
        return ModelClassroom(
            json['classroomName'],
            json['classroomId'],
        )