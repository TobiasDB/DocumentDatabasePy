import uuid


def get_client(conn_str):
    return "fake_client"


def get_database(client, db_name):
    return {}


async def ping(client):
    return True


async def get_one(db, collection, id):
    _c = db.get(collection)
    if _c is not None:
        return _c.get(id)
    return None


async def get(db, collection, ids):

    _c = db.get(collection)
    if _c is not None:
        if ids is not None:
            return [_c.get(id) for id in ids if _c.get(id) is not None]
        else:
            return _c.values()
    return []


async def put_one(db, collection, document):
    _c = db.get(collection)
    if _c is None:
        db[collection] = {}
    _id = str(uuid.uuid4())
    document["_id"] = _id
    db[collection][_id] = document
    return _id


async def put(db, collection, documents):
    _c = db.get(collection)
    if _c is None:
        db[collection] = {}
    ids = []
    for document in documents:
        _id = str(uuid.uuid4())
        document["_id"] = _id
        db[collection][_id] = document
        ids.append(_id)
    return ids


async def update_one(db, collection, id, document):
    _c = db.get(collection)
    if _c is not None:
        _d = _c.get(id)
        if _d is not None:
            _c[id] = {**_d, **document}
            return True
    return False


async def update(db, collection, ids, document):
    _c = db.get(collection)
    if _c is not None:
        returns = False
        for id in ids:
            _d = _c.get(id)
            if _d is not None:
                _c[id] = {**_d, **document}
                returns = True
        return returns

    return False


async def delete_one(db, collection, id):
    _c = db.get(collection)
    if _c is not None:
        _d = _c.get(id)
        if _d is not None:
            _c[id] = None
            del _c[id]
            return True
    return False


async def delete(db, collection, ids):
    _c = db.get(collection)
    if _c is not None:
        returns = False
        for id in ids:
            _d = _c.get(id)
            if _d is not None:
                _c[id] = None
                del _c[id]
                returns = True
        return returns
    return False
