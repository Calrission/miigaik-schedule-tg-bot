from abc import ABC

from data.models.model_classroom import ModelClassroom
from data.models.model_exam import ModelExam
from data.models.model_group import ModelGroup
from data.models.model_schedule_classroom import ModelScheduleClassroom
from data.models.model_schedule_group import ModelScheduleGroup
from data.models.model_schedule_teacher import ModelScheduleTeacher
from data.models.model_search_teacher import ModelSearchTeacher


class RemoteDataABC(ABC):

    def fetch_all_groups(self) -> list[ModelGroup]:
        pass

    def search_classrooms(self, name: str) -> list[ModelClassroom]:
        pass

    def search_group(self, group_name: str) -> list[dict]:
        pass

    def fetch_schedule_group(self, id_group: int, start_date: str, end_date: str) -> ModelScheduleGroup:
        pass

    def fetch_schedule_classroom(self, id_classroom: int, start_date: str, end_date: str) -> ModelScheduleClassroom:
        pass

    def fetch_schedule_teacher(self, id_teacher: int, start_date: str, end_date: str) -> ModelScheduleTeacher:
        pass

    def fetch_exams(self, group_id: int) -> list[ModelExam]:
        pass

    def search_teacher(self, teacher_name: str) -> list[ModelSearchTeacher]:
        pass
