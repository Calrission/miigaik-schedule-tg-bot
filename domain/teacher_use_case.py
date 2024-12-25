from data.models.model_search_teacher import ModelSearchTeacher
from loader import api
from presentation.view.view_error import ViewError


def search_teacher_by_name(name: str) -> list[ModelSearchTeacher] | ViewError:
    try:
        response: list[ModelSearchTeacher] = api.search_teacher(name)
        if len(response) == 0:
            return ViewError(f"Преподаватель '{name}' не найден. Попробуйте еще раз!")
        return response
    except Exception as e:
        return ViewError.something_went_wrong(e)
