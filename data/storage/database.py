import sqlite3
from typing import override
from data.models.model_group import ModelGroup
from data.storage.storage_abc import StorageABC
from data.storage.sqls import *


class Database(StorageABC):
    def __init__(self, name: str):
        self.con = sqlite3.connect(f"{name}.db")
        self.cur = self.con.cursor()

        self._prepare()

    def _prepare(self):
        self.cur.execute(CREATE_GROUP_TABLE)
        self.cur.execute(CREATE_FAVORITE_GROUP)
        self.con.commit()

    @override
    def insert_group(self, id_group: int, name_group: str, id_user: int, is_favorite: bool = False):
        self.cur.execute(INSERT_GROUP, (id_group, id_user, name_group))
        if is_favorite:
            self.set_favorite_group(id_user, id_group)
        self.con.commit()

    @override
    def delete_group(self, id_group: int, id_user: int):
        self.cur.execute(DELETE_GROUP, (id_group, id_user))
        self.con.commit()

    @override
    def set_favorite_group(self, id_user: int, id_group: int):
        current_favorite = self.fetch_favorite_user_group(id_user)
        if current_favorite is None:
            self.cur.execute(INSERT_FAVORITE, (id_user, id_group))
        else:
            self.cur.execute(UPDATE_FAVORITE, (id_group, id_user))
        self.con.commit()

    @override
    def fetch_user_groups(self, user_id: int) -> list[ModelGroup]:
        self.cur.execute(SELECT_USER_GROUPS, (user_id,))
        result = self.cur.fetchall()
        return [ModelGroup.from_db(i) for i in result]

    @override
    def fetch_favorite_user_group(self, user_id: int) -> ModelGroup | None:
        self.cur.execute(SELECT_USER_FAVORITE, (user_id,))
        result = self.cur.fetchall()
        return ModelGroup.from_db(result[0]) if result or len(result) != 0 else None

    def __del__(self):
        self.con.close()
