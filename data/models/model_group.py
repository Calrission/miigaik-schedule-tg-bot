import dataclasses


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

    def calc_link(self, current_time_unix: int) -> str:
        # 1703451600 - дата нулевой недели
        # 604800 - 7 дней
        current_index_link = (current_time_unix - 1703451600) // 604800
        return f"group/{self.id}/{current_index_link}"

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
