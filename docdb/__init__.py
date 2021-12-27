from importlib.metadata import version as v

from docdb.interface import DB  # noqa: F401
from docdb.errors import (  # noqa: F401
    DBError,
    DBConnectionError,
    ODMError,
    ODMHasNoDatabase,
    ODMNotLinkedToDatabase,
    ODMAlreadyLinkedToDatabase,
    ODMNotFoundInDatabase,
)
from docdb.odm import Document  # noqa: F401


def version():
    return v("docdb")
