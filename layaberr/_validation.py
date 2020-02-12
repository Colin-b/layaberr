from http import HTTPStatus
from typing import Union, List, Dict

from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse


class ModelCouldNotBeFound(HTTPException):
    """Corresponding model could not be found."""

    def __init__(self, requested_data):
        HTTPException.__init__(
            self,
            status_code=HTTPStatus.NOT_FOUND.value,
            detail="Corresponding model could not be found.",
        )
        self.requested_data = requested_data


DictErrors = Dict[str, List[str]]
ListErrors = Dict[int, DictErrors]


class ValidationFailed(HTTPException):
    """Validation failed."""

    def __init__(
        self,
        received_data: Union[List, Dict],
        errors: Union[ListErrors, DictErrors] = None,
        message: str = "",
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
        HTTPException.__init__(self, status_code=HTTPStatus.BAD_REQUEST.value)
        self.received_data = received_data
        self.errors = errors if errors else {"": [message]}


async def validation_failed_exception(request: Request, exc: ValidationFailed):
    """
    properties:
        fields:
            type: array
            items:
                required:
                    - field_name
                    - item
                properties:
                    item:
                        type: integer
                        description: Position of the item that could not be validated.
                        example: 1
                    field_name:
                        type: string
                        description: Name of the field that could not be validated.
                        example: sample_field_name
                    messages:
                        type: array
                        items:
                            type: string
                            description: Reason why the validation failed.
                            example: This is the reason why this field was not validated.
                type: object
    type: object
    """
    error_list = []
    for field_name_or_index, messages_or_fields in exc.errors.items():
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
    return JSONResponse({"fields": error_list}, status_code=exc.status_code)
