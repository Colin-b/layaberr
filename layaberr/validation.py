import logging
from http import HTTPStatus
from typing import Union, List, Dict

from flask_restplus import fields
from werkzeug.exceptions import BadRequest

logger = logging.getLogger(__name__)


def _bad_request_exception_model(api):
    exception_details = {
        "message": fields.String(
            description="Description of the error.",
            required=True,
            example="This is a description of the error.",
        )
    }
    return api.model("BadRequest", exception_details)


def add_bad_request_exception_handler(api):
    """
    Add the Bad Request Exception handler.

    :param api: The root Api
    """
    exception_model = _bad_request_exception_model(api)

    @api.errorhandler(BadRequest)
    @api.marshal_with(exception_model, code=HTTPStatus.BAD_REQUEST)
    def handle_exception(exception):
        """This is the Bad Request error handling."""
        logger.exception(HTTPStatus.BAD_REQUEST.description)
        return {"message": str(exception)}, HTTPStatus.BAD_REQUEST

    return HTTPStatus.BAD_REQUEST, HTTPStatus.BAD_REQUEST.description, exception_model


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


def _failed_field_validation_model(api):
    exception_details = {
        "item": fields.Integer(
            description="Position of the item that could not be validated.",
            required=True,
            example=1,
        ),
        "field_name": fields.String(
            description="Name of the field that could not be validated.",
            required=True,
            example="sample_field_name",
        ),
        "messages": fields.List(
            fields.String(
                description="Reason why the validation failed.",
                required=True,
                example="This is the reason why this field was not validated.",
            )
        ),
    }
    return api.model("FieldValidationFailed", exception_details)


def _failed_validation_model(api):
    exception_details = {
        "fields": fields.List(fields.Nested(_failed_field_validation_model(api)))
    }
    return api.model("ValidationFailed", exception_details)


def add_failed_validation_handler(api):
    """
    Add the default ValidationFailed handler.

    :param api: The root Api
    """
    exception_model = _failed_validation_model(api)

    @api.errorhandler(ValidationFailed)
    @api.marshal_with(exception_model, code=400)
    def handle_exception(failed_validation):
        """This is the default validation error handling."""
        logger.exception("Validation failed.")
        error_list = []
        for field_name_or_index, messages_or_fields in failed_validation.errors.items():
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
        return {"fields": error_list}, 400

    return 400, "Validation failed.", exception_model


class ModelCouldNotBeFound(Exception):
    def __init__(self, requested_data):
        self.requested_data = requested_data


def _model_could_not_be_found_model(api):
    exception_details = {
        "message": fields.String(
            description="Description of the error.",
            required=True,
            example="Corresponding model could not be found.",
        )
    }
    return api.model("ModelCouldNotBeFound", exception_details)


def add_model_could_not_be_found_handler(api):
    """
    Add the default ModelCouldNotBeFound handler.

    :param api: The root Api
    """
    exception_model = _model_could_not_be_found_model(api)

    @api.errorhandler(ModelCouldNotBeFound)
    @api.marshal_with(exception_model, code=404)
    def handle_exception(model_could_not_be_found):
        """This is the default model could not be found handling."""
        logger.exception("Corresponding model could not be found.")
        return {"message": "Corresponding model could not be found."}, 404

    return 404, "Corresponding model could not be found.", exception_model
