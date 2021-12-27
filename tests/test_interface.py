import pytest
from pydantic import ValidationError
import docdb


def test_db_variable_validation_invalid(db):
    """
    make sure that type validation is used on the
    arguments passed do a database object
    """
    with pytest.raises(ValidationError):
        _ = docdb.DB(None, "b")
    with pytest.raises(ValidationError):
        _ = docdb.DB("a", None)
    with pytest.raises(ValidationError):
        _ = db.get(None, None)
    with pytest.raises(ValidationError):
        _ = db.put(None, None)
    with pytest.raises(ValidationError):
        _ = db.update(None, None, None)
    with pytest.raises(ValidationError):
        _ = db.delete(None, None)


@pytest.mark.asyncio
async def test_db_interface_one(db):
    # test put one
    _id = await db.put_one("test", {"result1": True})
    assert (
        _id is not None
    ), "put_one failed to insert an object to the database / no id was returned"
    assert await db.get_one("test", _id) == {
        "_id": _id,
        "result1": True,
    }, "get_one failed to return the correct object"

    # test update one
    assert await db.update_one(
        "test", _id, {"result1": False}
    ), "update failed to execute"
    assert await db.get_one("test", _id) == {"_id": _id, "result1": False}

    # test delete one
    assert await db.delete_one("test", _id), "delete failed to execute"
    assert (
        await db.get_one("test", _id) is None
    ), "object was not deleted from the database"


@pytest.mark.asyncio
async def test_db_interface_many(db):
    # test put many
    ids = await db.put("test", [{"result1": True}, {"result2": True}])
    assert None not in ids, (
        "put_one failed to insert objects to the database "
        "/ not all ids where were returned"
    )

    results = await db.get("test", ids)
    assert results[0] == {
        "_id": ids[0],
        "result1": True,
    }, "get failed to return the correct objects"
    assert results[1] == {
        "_id": ids[1],
        "result2": True,
    }, "get failed to return the correct objects"

    # test update many
    assert await db.update("test", ids, {"result2": False}), "update failed to execute"

    results = await db.get("test", ids)
    assert results[0] == {
        "_id": ids[0],
        "result1": True,
        "result2": False,
    }, "update failed to update objects in the database"
    assert results[1] == {
        "_id": ids[1],
        "result2": False,
    }, "update failed to update objects in the database"

    # test delete many
    assert await db.delete("test", ids), "one or more deletes failed to execute"
    assert await db.get("test", ids) == [], "objects were not deleted from the database"
