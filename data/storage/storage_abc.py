from abc import ABC

from data.models.model_group import ModelGroup


class StorageABC(ABC):
    def insert_group(self, id_group: int, name_group: str, id_user: int, is_favorite: bool = False): pass

    def delete_group(self, id_group: int, id_user: int): pass

    def set_favorite_group(self, id_user: int, id_group: int): pass

    def fetch_user_groups(self, user_id: int) -> list[ModelGroup]: pass

    def fetch_favorite_user_group(self, user_id: int) -> ModelGroup | None: pass
