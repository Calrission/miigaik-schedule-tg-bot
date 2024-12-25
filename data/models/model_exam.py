import dataclasses
from datetime import datetime


@dataclasses.dataclass
class ModelExam:
    id: int
    student_group_id: int
    student_group_name: str
    classroom_id: int
    classroom_name: str
    classroom_floor: str
    classroom_building_name: str
    classroom_typename: str
    discipline_id: int
    discipline_name: str
    date_and_time: datetime
    examiner_id: int
    examiner_firstname: str
    examiner_lastname: str
    examiner_patronymic: str

    @staticmethod
    def from_json(data: dict):
        return ModelExam(
            id=data['id'],
            student_group_id=data['studentGroupId'],
            student_group_name=data['studentGroupName'],
            classroom_id=data['classroomId'],
            classroom_name=data['classroomName'],
            classroom_floor=data['classroomFloor'],
            classroom_building_name=data['classroomBuildingName'],
            classroom_typename=data['classroomTypeName'],
            discipline_id=data['disciplineId'],
            discipline_name=data['disciplineName'],
            date_and_time=datetime.strptime(data["dateAndTime"], "%Y-%m-%d %H:%M:%S"),
            examiner_id=data['examinerId'],
            examiner_firstname=data['examinerFirstName'],
            examiner_lastname=data['examinerLastName'],
            examiner_patronymic=data['examinerPatronymic'],
        )

    @property
    def datetime(self):
        return self.date_and_time.strftime("%d.%m.%Y %H:%M")

    @property
    def examiner_fio(self):
        return f"{self.examiner_lastname} {self.examiner_firstname} {self.examiner_patronymic}"

    def __str__(self):
        return f"""{self.datetime}
{self.discipline_name}\n{self.examiner_fio}
{'Аудитория ' if self.classroom_name != 'Военный учебный центр' else ''}{self.classroom_name} | {self.classroom_building_name} | {self.classroom_floor} этаж"""