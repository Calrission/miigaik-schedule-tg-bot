import dataclasses
import traceback


@dataclasses.dataclass
class ViewError:
    error: str
    exception: Exception | None = None

    @staticmethod
    def something_went_wrong(e: Exception):
        print(traceback.format_exc())
        return ViewError("Что-то пошло не так", e)
