from werkzeug.exceptions import NotFound

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