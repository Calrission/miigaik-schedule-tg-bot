from data.models.model_exam import ModelExam
from data.models.model_group import ModelGroup
from loader import api


def get_exams(group: ModelGroup) -> str:
    exams: list[ModelExam] = api.fetch_exams(group.id)

    def exam_bloc(exam: ModelExam) -> str:
        return f"""{exam.datetime}
{exam.discipline_name}\n{exam.examiner_fio}
{'Аудитория ' if exam.classroom_name != 'Военный учебный центр' else ''}{exam.classroom_name} | {exam.classroom_building_name} | {exam.classroom_floor} этаж"""

    return f"Экзамены {group.name}:\n\n{"\n\n".join(map(exam_bloc, exams))}"
