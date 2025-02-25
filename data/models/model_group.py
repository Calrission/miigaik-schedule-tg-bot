import dataclasses

from domain.utils import calc_current_start_end_date_week


@dataclasses.dataclass
class ModelGroup:
    name: str
    id: int

    @staticmethod
    def from_json(json: dict[str, str | int | bool | dict | float]) -> 'ModelGroup':
        return ModelGroup(
            name=json['groupName'],
            id=int(json['id'])
        )

    @staticmethod
    def from_db(date: tuple) -> 'ModelGroup':
        return ModelGroup(
            id=date[0],
            name=date[1]
        )

    def __post_init__(self):
        self._split = self.name.split("-")

    def split(self):
        return self._split

    def calc_link_group(self, current_time_unix: int) -> str:
        start_date, end_date = calc_current_start_end_date_week(current_time_unix)
        return f"group/{self.id}/?dateStart={start_date}&dateEnd={end_date}"

    @property
    def year(self):
        return int(self._split[0])

    @property
    def faculty(self):
        return self._split[1]

    @property
    def group(self):
        return self._split[2]

    @property
    def subgroup(self):
        return self._split[3]

    def __eq__(self, __value):
        if isinstance(__value, tuple) and len(__value) == 4:
            return self.year == __value[0] and self.faculty == __value[1] and self.group == __value[2] and self.subgroup == __value[3]
        return super().__eq__(__value)
