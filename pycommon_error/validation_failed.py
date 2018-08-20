import logging

from flask_restplus import fields

logger = logging.getLogger(__name__)


class ValidationFailed(Exception):
    def __init__(self, received_data, marshmallow_errors=None, message=''):
        self.received_data = received_data
        self.errors = marshmallow_errors if marshmallow_errors else {'': [message]}

    def __str__(self):
        return f'Errors: {self.errors}\nReceived: {self.received_data}'


def _failed_field_validation_model(api):
    exception_details = {
        'item': fields.Integer(description='Position of the item that could not be validated.',
                               required=True,
                               example=1),
        'field_name': fields.String(description='Name of the field that could not be validated.',
                                    required=True,
                                    example='sample_field_name'),
        'messages': fields.List(fields.String(description='Reason why the validation failed.',
                                              required=True,
                                              example='This is the reason why this field was not validated.')
                                ),
    }
    return api.model('FieldValidationFailed', exception_details)


def _failed_validation_model(api):
    exception_details = {
        'fields': fields.List(fields.Nested(_failed_field_validation_model(api))),
    }
    return api.model('ValidationFailed', exception_details)


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
        logger.exception('Validation failed.')
        error_list = []
        for field, messages in failed_validation.errors.items():
            item = 1
            field_name = field
            if isinstance(messages, dict):
                key, value = next(iter(messages.items()))
                field_name = key
                item = field + 1
                messages = value
            error_list.append({
                'item': item,
                'field_name': field_name,
                'messages': messages,
            })
        return {'fields': error_list}, 400

    return 400, 'Validation failed.', exception_model
