import logging

from flask_restplus import fields

logger = logging.getLogger(__name__)


class ModelCouldNotBeFound(Exception):
    def __init__(self, requested_data):
        self.requested_data = requested_data


def _model_could_not_be_found_model(api):
    exception_details = {
        'message': fields.String(description='Description of the error.',
                                 required=True,
                                 example='Corresponding model could not be found.'),
    }
    return api.model('ModelCouldNotBeFound', exception_details)


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
        logger.exception('Corresponding model could not be found.')
        return {'message': 'Corresponding model could not be found.'}, 404

    return 404, 'Corresponding model could not be found.', exception_model
