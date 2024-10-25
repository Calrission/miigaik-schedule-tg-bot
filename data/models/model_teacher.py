import dataclasses


@dataclasses.dataclass
class ModelTeacher:
    first_name: str
    last_name: str
    patronymic: str

    @staticmethod
    def from_json(json: dict[str, str]) -> 'ModelTeacher':
        return ModelTeacher(
            first_name=json['firstName'],
            last_name=json['lastName'],
            patronymic=json['patronymic'],
        )

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.patronymic}"