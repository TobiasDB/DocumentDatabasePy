import pytest
import docdb


@pytest.fixture(scope="function")
def db():
    """Create a database instance"""
    # Set the implementation to mocked
    docdb.interface.IMPLEMENTATION = docdb.implementations.mocked
    db = docdb.DB("conn_str", "db_name")
    yield db
    # close database
    # db.close() # Not Implemented


@pytest.fixture(scope="function")
def document(db):
    """Create a ODM Document"""

    class ODMDocument(docdb.Document):
        result1: bool

    ODMDocument.use(db, "test")
    yield ODMDocument
