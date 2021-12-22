from importlib.metadata import version

from docdb.interface import DB
from docdb.errors import DBError, DBConnectionError, ODMError, ODMHasNoDatabase, ODMNotLinkedToDatabase, ODMAlreadyLinkedToDatabase, ODMNotFoundInDatabase
from docdb.odm import Document


def version():
    return version('docdb')