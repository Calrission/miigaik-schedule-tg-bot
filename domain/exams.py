from data.models.model_exam import ModelExam
from data.models.model_group import ModelGroup
from loader import api


def get_exams(group: ModelGroup) -> str:
    exams: list[ModelExam] = api.fetch_exams(group.id)

    return f"Экзамены {group.name}:\n\n{"\n\n".join(map(str, exams))}"
