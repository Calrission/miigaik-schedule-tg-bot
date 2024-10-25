import dataclasses

from data.models.model_teacher import ModelTeacher


@dataclasses.dataclass
class ModelTeacherId:
    id: int
    teacher: ModelTeacher

    @staticmethod
    def from_json(json: dict[str, dict | int | str]) -> 'ModelTeacherId':
        return ModelTeacherId(
            id=int(json['id']),
            teacher=ModelTeacher.from_json(json['teacher']),
        )
