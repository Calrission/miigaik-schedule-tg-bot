from typing import override
import requests
from data.models.model_classroom import ModelClassroom
from data.models.model_exam import ModelExam
from data.models.model_group import ModelGroup
from data.models.model_schedule_classroom import ModelScheduleClassroom
from data.models.model_schedule_group import ModelScheduleGroup
from data.models.model_schedule_teacher import ModelScheduleTeacher
from data.models.model_search_teacher import ModelSearchTeacher
from data.models.model_teacher import ModelTeacher
from data.repositories.remote_data_abc import RemoteDataABC


class RemoteData(RemoteDataABC):
    def __init__(self):
        self.base_url = "https://study.miigaik.ru/api/v1/"

    @override
    def fetch_all_groups(self) -> list[ModelGroup]:
        url = self.base_url + "search/group"
        response = requests.get(url, params={"groupName": ""})
        response.raise_for_status()
        data = response.json()
        return [ModelGroup.from_json(i) for i in data]

    @override
    def search_classrooms(self, name: str) -> list[ModelClassroom]:
        url = self.base_url + "search/classroom"
        response = requests.get(url, params={"classroomName": name})
        response.raise_for_status()
        data = response.json()
        return [ModelClassroom.from_json(i) for i in data]

    @override
    def fetch_schedule_classroom(self, id_classroom: str, start_date: str, end_date: str) -> ModelScheduleClassroom:
        url = self.base_url + f"classroom/{id_classroom}?dateStart={start_date}&dateEnd={end_date}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return ModelScheduleClassroom.from_json(data)

    @override
    def search_group(self, group_name: str) -> list[dict]:
        url = self.base_url + f"search/group"
        response = requests.get(url, params={"groupName": group_name})
        response.raise_for_status()
        return response.json()

    @override
    def fetch_schedule_group(self, id_schedule: str, start_date: str, end_date: str) -> ModelScheduleGroup:
        url = self.base_url + f"group/{id_schedule}?dateStart={start_date}&dateEnd={end_date}"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        return ModelScheduleGroup.from_json(json)

    @override
    def fetch_exams(self, group_id: int) -> list[ModelExam]:
        url = self.base_url + f"exam?student_group_id={group_id}"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        return [ModelExam.from_json(i) for i in json]

    @override
    def fetch_schedule_teacher(self, id_teacher: int, start_date: str, end_date: str) -> ModelScheduleTeacher:
        url = self.base_url + f"teacher/{id_teacher}?dateStart={start_date}&dateEnd={end_date}"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        return ModelScheduleTeacher.from_json(json)

    @override
    def search_teacher(self, teacher_name: str) -> list[ModelSearchTeacher]:
        url = self.base_url + f"search/teacher?teacherFullName={teacher_name}"
        response = requests.get(url)
        response.raise_for_status()
        json = response.json()
        return [ModelSearchTeacher.from_json(i) for i in json]
