from abc import ABC

from data.models.model_classroom import ModelClassroom
from data.models.model_exam import ModelExam
from data.models.model_group import ModelGroup
from data.models.model_schedule_classroom import ModelScheduleClassroom
from data.models.model_schedule_group import ModelScheduleGroup


class RemoteDataABC(ABC):

    def fetch_all_groups(self) -> list[ModelGroup]:
        pass

    def search_classrooms(self, name: str) -> list[ModelClassroom]:
        pass

    def search_group(self, group_name: str) -> list[dict]:
        pass

    def fetch_schedule_group(self, current_week_schedule_link: str) -> ModelScheduleGroup:
        pass

    def fetch_schedule_classroom(self, current_week_schedule_link: str) -> ModelScheduleClassroom:
        pass

    def fetch_exams(self, group_id: int) -> list[ModelExam]:
        pass
