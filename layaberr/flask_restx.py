from typing import Union, List, Dict, Type
import logging
import http

import flask_restx
from werkzeug.exceptions import Unauthorized, Forbidden, BadRequest


logger = logging.getLogger(__name__)


def add_error_handler(
    api: flask_restx.Api, exception: Type[Exception], http_status: http.HTTPStatus
):
    """
    Subscribe error handler for the provided exception class.

    :param api: The Flask-RestX API that will handle this exception.
    :param exception: The exception class to handle.
    :param http_status: The http.HTTPStatus of the response.
    :return: A tuple that can be used to document this error handler in flask_restx.
    As in @api.response(*error_response)
    """

    @api.errorhandler(exception)
    @api.response(
        code=http_status.value, description=None, model=flask_restx.fields.String
    )
    def handle_exception(e):
        return str(e), http_status.value

    return http_status.value, http_status.description, flask_restx.fields.String


class ValidationFailed(Exception):
    def __init__(
        self, received_data: Union[List, Dict], errors: Dict = None, message: str = ""
    ):
        """
        Represent a client data validation error.

        :param received_data: Data triggering the error. Should be a list or a dictionary in most cases.
        :param errors: To be used if a specific field triggered the error.
        If received_data is a list:
            key is supposed to be the index in received_data
            value is supposed to be a the same as if received_data was the dictionary at this index
        If received_data is a dict:
            key is supposed to be the field name in error
            value is supposed to be a list of error messages on this field
        :param message: The error message in case errors cannot be provided.
        """
        self.received_data = received_data
        self.errors = errors if errors else {"": [message]}

    def __str__(self):
        return f"Errors: {self.errors}\nReceived: {self.received_data}"

    @staticmethod
    def to_list(errors: dict) -> List[dict]:
        error_list = []
        for field_name_or_index, messages_or_fields in errors.items():
            if isinstance(messages_or_fields, dict):
                error_list.extend(
                    [
                        {
                            "item": field_name_or_index + 1,
                            "field_name": field_name,
                            "messages": messages,
                        }
                        for field_name, messages in messages_or_fields.items()
                    ]
                )
            else:
                error_list.append(
                    {
                        "item": 1,
                        "field_name": field_name_or_index,
                        "messages": messages_or_fields,
                    }
                )
        return error_list

    @staticmethod
    def list_item_model():
        return {
            "item": flask_restx.fields.Integer(
                description="Position of the item that could not be validated.",
                example=1,
            ),
            "field_name": flask_restx.fields.String(
                description="Name of the field that could not be validated.",
                example="sample_field_name",
            ),
            "messages": flask_restx.fields.List(
                flask_restx.fields.String(
                    description="Reason why the validation failed.",
                    example="This is the reason why this field was not validated.",
                )
            ),
        }


def add_failed_validation_handler(api: flask_restx.Api):
    """
    Subscribe error handler for the layaberr.flask_restx.ValidationFailed exception.

    :param api: The Flask-RestX API that will handle this exception.
    :return: A tuple that can be used to document this error handler in flask_restx.
    As in @api.response(*error_response)
    """
    list_item_model = api.model("ValidationFailed", ValidationFailed.list_item_model())

    @api.errorhandler(ValidationFailed)
    @api.response(
        code=http.HTTPStatus.BAD_REQUEST.value,
        description=None,
        model=[list_item_model],
    )
    def handle_exception(failed_validation):
        return (
            ValidationFailed.to_list(failed_validation.errors),
            http.HTTPStatus.BAD_REQUEST.value,
        )

    return http.HTTPStatus.BAD_REQUEST.value, "Validation failed.", [list_item_model]


def add_error_handlers(api: flask_restx.Api) -> Dict[str, dict]:
    """
    Subscribe error handlers for:
        * werkzeug.exceptions.BadRequest
        * layaberr.flask_restx.ValidationFailed
        * werkzeug.exceptions.Unauthorized
        * werkzeug.exceptions.Forbidden
        * Exception

    :param api: The Flask-RestX API that will handle those exceptions.
    :return: A dictionary that can be used to document those error handlers in flask_restx.
    As in @api.doc(**error_responses)
    """
    add_error_handler(api, BadRequest, http.HTTPStatus.BAD_REQUEST)
    failed_validation = add_failed_validation_handler(api)
    unauthorized = add_error_handler(api, Unauthorized, http.HTTPStatus.UNAUTHORIZED)
    forbidden = add_error_handler(api, Forbidden, http.HTTPStatus.FORBIDDEN)
    exception = add_error_handler(api, Exception, http.HTTPStatus.INTERNAL_SERVER_ERROR)

    return {
        "responses": {
            failed_validation[0]: (failed_validation[1], failed_validation[2]),
            unauthorized[0]: (unauthorized[1], unauthorized[2]),
            forbidden[0]: (forbidden[1], forbidden[2]),
            exception[0]: (exception[1], exception[2]),
        }
    }
