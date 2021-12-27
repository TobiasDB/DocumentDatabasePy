class DBError(Exception):
    pass


class DBConnectionError(DBError):
    pass


class ODMError(Exception):
    pass


class ODMHasNoDatabase(ODMError):
    pass


class ODMNotLinkedToDatabase(ODMError):
    pass


class ODMAlreadyLinkedToDatabase(ODMError):
    pass


class ODMNotFoundInDatabase(ODMError):
    pass
