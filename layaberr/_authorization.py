import logging
from http import HTTPStatus

from flask_restplus import fields
from werkzeug.exceptions import Unauthorized, Forbidden

logger = logging.getLogger(__name__)


def _unauthorized_exception_model(api):
    exception_details = {
        "message": fields.String(
            description="Description of the error.",
            required=True,
            example="This is a description of the error.",
        )
    }
    return api.model("Unauthorized", exception_details)


def add_unauthorized_exception_handler(api):
    """
    Add the Unauthorized Exception handler.

    :param api: The root Api
    """
    exception_model = _unauthorized_exception_model(api)

    @api.errorhandler(Unauthorized)
    @api.marshal_with(exception_model, code=HTTPStatus.UNAUTHORIZED)
    def handle_exception(exception):
        """This is the Unauthorized error handling."""
        logger.exception(HTTPStatus.UNAUTHORIZED.description)
        return {"message": str(exception)}, HTTPStatus.UNAUTHORIZED

    return HTTPStatus.UNAUTHORIZED, HTTPStatus.UNAUTHORIZED.description, exception_model


def add_forbidden_exception_handler(api):
    """
    Add the Forbidden Exception handler.

    :param api: The root Api
    """
    exception_model = _unauthorized_exception_model(api)

    @api.errorhandler(Forbidden)
    @api.marshal_with(exception_model, code=HTTPStatus.FORBIDDEN)
    def handle_exception(exception):
        """This is the Forbidden error handling."""
        logger.exception(HTTPStatus.FORBIDDEN.description)
        return {"message": str(exception)}, HTTPStatus.FORBIDDEN

    return HTTPStatus.FORBIDDEN, HTTPStatus.FORBIDDEN.description, exception_model
