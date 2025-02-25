import dataclasses

from data.models.model_teacher import ModelTeacher


@dataclasses.dataclass
class ModelSearchTeacher:
    id: int
    teacher: ModelTeacher

    @staticmethod
    def from_json(data: dict) -> 'ModelSearchTeacher':
        return ModelSearchTeacher(
            id=data['id'],
            teacher=ModelTeacher.from_json(data['teacher']),
        )

    def __str__(self) -> str:
        return str(self.teacher)

