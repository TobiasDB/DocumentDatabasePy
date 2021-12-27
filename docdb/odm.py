from __future__ import annotations
from pydantic import BaseModel, Field
from pydantic.main import ModelMetaclass
from typing import List, Union, Optional, ClassVar
from pydantic import validate_arguments

from docdb.interface import DB
from docdb.errors import (
    ODMHasNoDatabase,
    ODMNotLinkedToDatabase,
    ODMAlreadyLinkedToDatabase,
    ODMNotFoundInDatabase,
)


class DocumentMetaclass(ModelMetaclass):
    @property
    def db(cls):
        return cls._db

    @property
    def collection(cls):
        return cls._collection

    @validate_arguments
    def use(cls, db, collection: str):
        cls._db = db
        cls._collection = collection

    @validate_arguments
    async def gets(cls, ids: Optional[Union[str, List[str]]] = None):
        if isinstance(ids, str):
            result = await cls.db.get_one(cls.collection, ids)
            if result is not None:
                return cls(**result)
        elif isinstance(ids, list):
            result = await cls.db.get(cls.collection, ids)
            if result is not None:
                return [cls(**doc) for doc in result]
        else:
            result = await cls.db.get(cls.collection, None)
            if result is not None:
                return [cls(**doc) for doc in result]
        return None

    @validate_arguments
    async def puts(cls, documents: Union[dict, List[dict]]):
        if isinstance(documents, dict):
            return await cls.db.put_one(cls.collection, documents)
        else:
            return await cls.db.put(cls.collection, documents)

    @validate_arguments
    async def updates(cls, ids: Union[str, List[str]], document: dict):
        if isinstance(ids, str):
            return await cls.db.update_one(cls.collection, ids, document)
        else:
            return await cls.db.update(cls.collection, ids, document)

    @validate_arguments
    async def deletes(cls, ids: Union[str, List[str]]):
        if isinstance(ids, str):
            return await cls.db.delete_one(cls.collection, ids)
        else:
            return await cls.db.delete(cls.collection, ids)


class Document(BaseModel, metaclass=DocumentMetaclass):
    _db: ClassVar[DB] = None
    _collection: ClassVar[str] = None

    id: str = Field(None, alias="_id")

    class Config:
        validate_all = True
        validate_assignment = True
        allow_population_by_field_name = True

    async def get(self):
        if not self.__has_database():
            raise ODMHasNoDatabase()
        elif not self.__has_id():
            raise ODMNotLinkedToDatabase()

        updated = await self.__class__.gets(self.id)
        if updated is None:
            raise ODMNotFoundInDatabase()
        self.__reload(updated.document())
        return self

    async def put(self):
        if not self.__has_database():
            raise ODMHasNoDatabase()
        elif self.__has_id():
            raise ODMAlreadyLinkedToDatabase()

        result = await self.__class__.puts(self.document())
        self.id = result
        return result

    async def update(self):
        if not self.__has_database():
            raise ODMHasNoDatabase()
        elif not self.__has_id():
            raise ODMNotLinkedToDatabase()

        result = await self.__class__.updates(self.id, self.document())
        if not result:
            raise ODMNotFoundInDatabase()
        return result

    async def delete(self):
        if not self.__has_database():
            raise ODMHasNoDatabase()
        elif not self.__has_id():
            raise ODMNotLinkedToDatabase()

        result = await self.__class__.deletes(self.id)
        if not result:
            raise ODMNotFoundInDatabase()
        self.id = None
        return result

    def document(self):
        return self.dict(by_alias=True, exclude_defaults=True)

    def __has_database(self):
        if self.__class__.db is None or self.__class__.collection is None:
            return False
        return True

    def __has_id(self):
        if self.id is None:
            return False
        return True

    def __reload(self, document):
        object.__setattr__(self, "__dict__", {**self.__dict__, **document})
