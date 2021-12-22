
from pydantic import validate_arguments
from typing import List

import implementations

IMPLEMENTATION = implementations.mongo

class Client:
    lazyload = False

    @validate_arguments
    def __init__(self, conn_str: str) -> None:
        self._conn_str = conn_str
        self.__lazy_client = None
        if not Client.lazyload:
            self._client

    @property
    def _client(self):
        """ Lazy Connection """
        if self.__lazy_client is None:
            self.__lazy_client = IMPLEMENTATION.get_client(self.__conn_str)
        return self.__lazy_client

    async def ping(self):
        """ Ping the database to test connectivity """
        return IMPLEMENTATION.ping(self._client)


class DB(Client):
    lazyload = False
    @validate_arguments
    def __init__(self, conn_str: str, db_name) -> None:
        super().__init__(conn_str)
        self._db_name = db_name

        self.__lazy_db = None
        if not DB.lazyload:
            self._db

    @property
    def _db(self):
        """ Lazy Cursor """
        if self.__lazy_db is None:
            self.__lazy_db = IMPLEMENTATION.get_database(self._client, self._db_name)
        return self.__lazy_db

    @validate_arguments
    async def get_one(self, collection: str, id: str) -> dict:
        return await IMPLEMENTATION.get_one(self._db, collection, id)

    @validate_arguments
    async def get(self, collection: str, ids: List[str]) -> List[dict]:
        return await IMPLEMENTATION.get(self._db, collection, ids)

    @validate_arguments
    async def put_one(self, collection: str, document: dict) -> str:
        return await IMPLEMENTATION.put_one(self._db, collection, document)

    @validate_arguments
    async def put(self, collection: str, documents: List[dict]) -> List[str]:
        return await IMPLEMENTATION.put(self._db, collection, documents)

    @validate_arguments
    async def update_one(self, collection: str, id: str, document: dict) -> bool:
        return await IMPLEMENTATION.update_one(self._db, collection, id, document)

    @validate_arguments
    async def update(self, collection: str, ids: List[str], document: dict) -> bool:
        return await IMPLEMENTATION.update(self._db, collection, ids, document)

    @validate_arguments
    async def delete_one(self, collection: str, id: str) -> bool:
        return await IMPLEMENTATION.delete_one(self._db, collection, id)

    @validate_arguments
    async def delete(self, collection: str, ids: List[str]) -> bool:
        return await IMPLEMENTATION.delete_one(self._db, collection, ids)



