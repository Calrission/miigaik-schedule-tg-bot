import dataclasses


@dataclasses.dataclass
class ViewError:
    error: str
    exception: Exception | None = None

    @staticmethod
    def something_went_wrong(e: Exception):
        return ViewError("Что-то пошло не так", e)
