import pytest
from pydantic import ValidationError
import docdb


@pytest.mark.asyncio
async def test_odm_variable_validation_invalid(document):
    """
    make sure that type validation is used
    on the arguments passed do a odm object"""
    with pytest.raises(ValidationError):
        _ = document.use(None, None)
    with pytest.raises(ValidationError):
        _ = await document.puts(None)
    with pytest.raises(ValidationError):
        _ = await document.updates(None, None)
    with pytest.raises(ValidationError):
        _ = await document.deletes(None)


@pytest.mark.asyncio
async def test_odm_class_interface_one(document):
    # test put many
    _id = await document.puts({"result1": True})
    assert _id is not None, "Documents was not inserted"

    # Test getting all
    docs = await document.gets()
    print(docs)
    assert len(docs) == 1, "Too many documents found in database after insert"
    for doc in docs:
        print(doc)
        assert doc.id == _id, "Documents could not be fetched"

    # Test getting by ids
    doc = await document.gets(_id)
    assert doc.id == _id, "Document could not be fetched by ID"

    # Test updaing
    success = await document.updates(_id, {"result1": False})
    assert success, "Document refused to be updated"

    docs = await document.gets()
    for doc in docs:
        assert doc.result1 is False, "Document was not updated"

    # Test Deleteting
    success = await document.deletes(_id)
    assert success, "Documents refused to be deleted"
    docs = await document.gets()
    assert len(docs) == 0, "Documents was not deleted"


@pytest.mark.asyncio
async def test_odm_class_interface_many(document):
    # test put many
    ids = await document.puts([{"result1": True}, {"result1": True}])
    assert len(ids) == 2, "Not all documents were inserted"

    # Test getting all
    docs = await document.gets()

    for doc in docs:
        assert doc.id in ids, "Documents could not be fetched"

    # Test getting by ids
    docs = await document.gets(ids)

    for doc in docs:
        assert doc.id in ids, "Documents could not be fetched by ID"

    # Test updaing
    success = await document.updates(ids, {"result1": False})
    assert success, "Documents refused to be updated"

    docs = await document.gets()
    for doc in docs:
        assert doc.result1 is False, "Documents were not updated"

    # Test Deleteting
    success = await document.deletes(ids)
    assert success, "Documents refused to be deleted"
    docs = await document.gets()
    assert len(docs) == 0, "Documents were not deleted"


@pytest.mark.asyncio
async def test_odm_object_interface(document):
    # test put many
    doc = document(**{"result1": True})
    assert doc.id is None, "Document had a ID before it was added to the database"

    _id = await doc.put()
    assert _id is not None, "Document was not inserted"
    assert doc.id == _id, "Document ID did not match"

    with pytest.raises(docdb.ODMAlreadyLinkedToDatabase):
        _ = await doc.put()

    doc.result1 = False
    success = await doc.update()
    assert success, "Update was reported as failure"
    assert doc.result1 is False, "Attribute of object changed unexpectedly"

    success = await document.updates(_id, {"result1": True})
    assert success is True, "Documents refused to be updated"
    await doc.get()
    assert doc.result1 is True, "Document was not updated to match database state"

    success = await doc.delete()
    assert success is True, "Document refused to be deleted"
    assert doc.id is None, "Id was not removed from object after deletion"

    doc = await document.gets(_id)
    assert doc is None, "Document was not properly deleted"
