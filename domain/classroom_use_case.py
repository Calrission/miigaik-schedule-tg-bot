from data.models.model_classroom import ModelClassroom
from loader import api
from presentation.view.view_error import ViewError


def search_classroom(classroom_name: str) -> ViewError | list[ModelClassroom]:
    try:
        response: list[ModelClassroom] = api.search_classrooms(classroom_name)
        if len(response) == 0:
            return ViewError(f"Аудитория с названием '{classroom_name}' не найдена. Попробуйте еще раз!")
        return response
    except Exception as e:
        return ViewError.something_went_wrong(e)
