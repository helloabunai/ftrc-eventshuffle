from werkzeug.exceptions import NotFound, Conflict

class JSONException(Exception):
    """
    :param status_code: response status_code
    :param message: exception message
    """
    status_code = NotFound.code
    message = ''

    def __init__(self, message=None, status_code=None):
        Exception.__init__(self)
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {
            'error': {
                'code': self.status_code,
                'message': self.message,
                'type': str(self.__class__.__name__)
            }
        }

class FailedJSONSchemaValidationException(JSONException):
    """
    Raised if a JSON POST payload incoming from 
    client failed schema validation
    """
    pass

class DatabaseError(JSONException):
    """
    Generic database interaction error.
    Inherit this error for all subsequent
    errors that are related to database.
    """
    pass


class RecordNotFound(DatabaseError):
    """
    Raised when the record was not found in the database.
    """
    pass


class RecordAlreadyExists(DatabaseError):
    """
    Raised in the case of violation of a unique constraint.
    """
    status_code = Conflict.code