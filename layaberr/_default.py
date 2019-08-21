import logging
from http import HTTPStatus

from flask_restplus import fields

logger = logging.getLogger(__name__)


def _exception_model(api):
    exception_details = {
        "message": fields.String(
            description="Description of the error.",
            required=True,
            example="This is a description of the error.",
        )
    }
    return api.model("Exception", exception_details)


def add_exception_handler(api):
    """
    Add the default Exception handler.

    :param api: The root Api
    """
    exception_model = _exception_model(api)

    @api.errorhandler(Exception)
    @api.marshal_with(exception_model, code=HTTPStatus.INTERNAL_SERVER_ERROR)
    def handle_exception(exception):
        """This is the default error handling."""
        logger.exception("An unexpected error occurred.")
        return {"message": str(exception)}, HTTPStatus.INTERNAL_SERVER_ERROR

    return (
        HTTPStatus.INTERNAL_SERVER_ERROR,
        "An unexpected error occurred.",
        exception_model,
    )
