from bson.codec_options import CodecOptions
import pymongo.errors
from motor.motor_asyncio import AsyncIOMotorClient
import datetime
from bson.objectid import ObjectId


def get_client(conn_str):
    return AsyncIOMotorClient(
        conn_str,
        connectTimeoutMS=20000,
        waitQueueTimeoutMS=20000,
        socketTimeoutMS=60000,
    )


def get_database(client, db_name):
    # Add timezone info to datatime objects in database
    codec_options = CodecOptions(tz_aware=True, tzinfo=datetime.timezone.utc)
    # Create a cursor
    return client[db_name].with_options(codec_options)


def _parse_filter(_filter):
    _filter = _filter or {}
    if (_id := _filter.get("_id")) is not None:

        _filter["_id"] = ObjectId(_id)
    return _filter


def _parse_dict(_dict):
    _dict = _dict or {}
    if "_id" in _dict.keys():
        _dict["_id"] = None
        del _dict["_id"]
    return _dict


async def ping(client):
    try:
        _ = await client.admin.command({"ping": 1})
    except pymongo.errors.ConnectionFailure:
        return False
    return True


async def get_one(db, collection, id):
    _filter = _parse_filter({"_id": id})
    document = await db[collection].find_one(_filter)
    if document is None:
        return None

    # serialize bson ObjectId to string
    _id = document.get("_id")
    if _id is not None:
        document["_id"] = str(_id)
    return document


async def get(db, collection, ids):
    _filter = _parse_filter({"_id": {"$in": ids}})
    documents = []
    # serialize bson ObjectId to string in each result
    async for doc in db[collection].find(_filter):
        _id = doc.get("_id")
        if _id is not None:
            doc["_id"] = str(_id)
        documents.append(doc)
    return documents


async def put_one(db, collection, document):
    document = _parse_dict(document)
    result = await db[collection].insert_one(document)
    return str(result.inserted_id)


async def put(db, collection, documents):
    for document in documents:
        document = _parse_dict(document)
    result = await db[collection].insert_many(documents)
    return [str(_id) for _id in result.inserted_ids]


async def update_one(db, collection, id, document):
    _filter = _parse_filter({"_id": id})
    document = _parse_dict(document)
    result = await db[collection].update_one(_filter, {"$set": document})
    if result.matched_count:
        return True
    return False


async def update(db, collection, ids, document):
    _filter = _parse_filter({"_id": {"$in": ids}})
    document = _parse_dict(document)
    result = await db[collection].update_many(_filter, {"$set": document})
    if result.matched_count:
        return True
    return False


async def delete_one(db, collection, id):
    _filter = _parse_filter({"_id": id})
    result = await db[collection].delete_one(_filter)
    if result.deleted_count:
        return True
    return False


async def delete(db, collection, ids):
    _filter = _parse_filter({"_id": {"$in": ids}})
    result = await db[collection].delete_many(_filter)
    if result.deleted_count:
        return True
    return False
