import logging
import sys

from flask import Flask
from flask_restplus import Resource, Api
from pycommon_test.service_tester import JSONTestCase
from werkzeug.exceptions import Unauthorized, BadRequest

from pycommon_error import validation, authorization, default

logging.basicConfig(
    format='%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.DEBUG)
logging.getLogger('sqlalchemy').setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


class TestErrorHandling(JSONTestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        api = Api(app)

        bad_request_response = validation.add_bad_request_exception_handler(api)
        unauthorized_response = authorization.add_unauthorized_exception_handler(api)
        model_not_found_response = validation.add_model_could_not_be_found_handler(api)
        validation_failed_response = validation.add_failed_validation_handler(api)
        default_response = default.add_exception_handler(api)

        @api.route('/unauthorized')
        class UnauthorizedError(Resource):
            @api.response(*unauthorized_response)
            @api.response(*default_response)
            def get(self):
                raise Unauthorized

        @api.route('/bad_request')
        class BadRequestError(Resource):
            @api.response(*bad_request_response)
            @api.response(*default_response)
            def get(self):
                raise BadRequest

        @api.route('/model_not_found')
        class ModelNotFoundError(Resource):
            @api.response(*model_not_found_response)
            @api.response(*default_response)
            def get(self):
                row = {'value': 'my_value1'}
                raise validation.ModelCouldNotBeFound(row)

        @api.route('/validation_failed_item')
        class ValidationFailedItemError(Resource):
            @api.response(*validation_failed_response)
            @api.response(*default_response)
            def get(self):
                received_data = {'optional_string_value': 'my_value1', 'mandatory_integer_value': 1,
                                 'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23',
                                 'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                 'optional_float_value': 100}, {'optional_string_value': 'my_value2',
                                                                'optional_enum_value': 'First Enum Value',
                                                                'optional_date_value': '2017-10-23',
                                                                'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                                                'optional_float_value': 200}
                errors = {'mandatory_integer_value': ['Missing data for required field.']}
                raise validation.ValidationFailed(received_data, marshmallow_errors=errors)

        @api.route('/validation_failed_list')
        class ValidationFailedListError(Resource):
            @api.response(*validation_failed_response)
            @api.response(*default_response)
            def get(self):
                received_data = [{'optional_string_value': 'my_value1', 'mandatory_integer_value': 1,
                                  'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23',
                                  'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                  'optional_float_value': 100},
                                 {'optional_string_value': 'my_value2', 'optional_enum_value': 'First Enum Value',
                                  'optional_date_value': '2017-10-23',
                                  'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00',
                                  'optional_float_value': 200}]
                errors = {1: {'mandatory_integer_value': ['Missing data for required field.']}}
                raise validation.ValidationFailed(received_data, marshmallow_errors=errors)

        @api.route('/default_error')
        class DefaultError(Resource):
            @api.response(*bad_request_response)
            @api.response(*validation_failed_response)
            @api.response(*model_not_found_response)
            @api.response(*unauthorized_response)
            @api.response(*default_response)
            def get(self):
                raise Exception

        return app

    def test_unauthorized(self):
        response = self.client.get('/unauthorized')
        self.assert401(response)
        self.assert_json(response, {
            'message': "401 Unauthorized: The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required."})

    def test_bad_request(self):
        response = self.client.get('/bad_request')
        self.assert400(response)
        self.assert_json(response, {
            'message': '400 Bad Request: The browser (or proxy) sent a request that this server could not understand.'})

    def test_model_not_found(self):
        response = self.client.get('/model_not_found')
        self.assert404(response)
        self.assert_json(response, {
            'message': 'Corresponding model could not be found. You have requested this URI [/model_not_found] but did you mean /model_not_found ?'})

    def test_default(self):
        response = self.client.get('/default_error')
        self.assert500(response)
        self.assert_json(response, {'message': ''})

    def test_validation_failed_item(self):
        response = self.client.get('/validation_failed_item')
        self.assert400(response)
        self.assert_json(response, {'fields': [
            {'item': 1, 'field_name': 'mandatory_integer_value', 'messages': ['Missing data for required field.']}],
            'message': "Errors: {'mandatory_integer_value': ['Missing data for required field.']}\nReceived: ({'optional_string_value': 'my_value1', 'mandatory_integer_value': 1, 'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23', 'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00', 'optional_float_value': 100}, {'optional_string_value': 'my_value2', 'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23', 'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00', 'optional_float_value': 200})"})

    def test_validation_failed_list(self):
        response = self.client.get('/validation_failed_list')
        self.assert400(response)
        self.assert_json(response, {'fields': [
            {'item': 2, 'field_name': 'mandatory_integer_value', 'messages': ['Missing data for required field.']}],
            'message': "Errors: {1: {'mandatory_integer_value': ['Missing data for required field.']}}\nReceived: [{'optional_string_value': 'my_value1', 'mandatory_integer_value': 1, 'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23', 'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00', 'optional_float_value': 100}, {'optional_string_value': 'my_value2', 'optional_enum_value': 'First Enum Value', 'optional_date_value': '2017-10-23', 'optional_date_time_value': '2017-10-24T21:46:57.12458+00:00', 'optional_float_value': 200}]"})
