import os
import json
import inspect
import jsonschema
from flask import request
from functools import wraps

from project.common.exceptions import FailedJSONSchemaValidationException

schemas_dir = 'schemas/'
schemas_path = os.path.join(os.getcwd(), schemas_dir)

def get_request_payload(method):
    """Get request payload based on the
    request.method.
    """
    return {
        'GET': _get_url_params_as_dict,
        'POST': _get_request_body
    }[method]


def _get_url_params_as_dict(_request):
    """
    Get url query params as `dict`.
    """
    return _multi_dict_to_dict(_request.args)


def _get_request_body(_request):
    """
    Get the json payload of the request.
    """
    return _request.json


def _multi_dict_to_dict(_md):
    """Converts a `MultiDict` to a
    `dict` object.
    :param _md: object
    :type _md: MultiDict
    :returns: converted MultiDict object
    :rtype: dict
    """
    result = dict(_md)
    for key, value in result.items():
        if len(value) == 1:
            result[key] = serialize_number(value[0])
        else:
            result[key] = [serialize_number(v) for v in value]
    return result


def serialize_number(value):
    """
    cast string to int + return, if fail,
    string to float + return, if fail
    return string
    """
    try:
        _val = int(value)
    except ValueError:
        pass
    try:
        _val = float(value)
    except ValueError:
        return value
    return _val


def get_schema(path):
    """
    Read a .json file and return its content.
    """
    with open(path, 'r') as f:
        return json.load(f)


def validate_schema(payload, schema):
    """
    :param payload: incoming request data
    :type payload: dict
    :param schema: the schema the request payload should
                   be validated against
    :type schema: .json file
    :returns: errors if any
    :rtype: list
    """
    errors = []
    validator = jsonschema.Draft4Validator(
        schema,
        format_checker=jsonschema.FormatChecker()
    )
    for error in sorted(validator.iter_errors(payload), key=str):
        errors.append(error.message)

    return errors


def _get_path_for_function(func):
    return os.path.dirname(os.path.realpath(inspect.getfile(func)))

def schema(path=None):

    """
    Validate the request body against a schema.
    :param path: path to the schema file
    :type path: string
    :returns: list of errors if there are any
    :raises: WorkInProgressException if there are any errors

    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            _path = path.lstrip('/')            
            schema_path = os.path.join(schemas_path, _path)
            payload = get_request_payload(request.method)(request)

            errors = validate_schema(payload, get_schema(schema_path))
            if errors:
               raise FailedJSONSchemaValidationException(message=errors)

            return func(*args, **kwargs)
        return wrapped
    return decorator

