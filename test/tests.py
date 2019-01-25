import logging
import sys

from flask import Flask
from flask_restplus import Resource, Api
from pycommon_test.service_tester import JSONTestCase
from werkzeug.exceptions import Unauthorized, BadRequest, Forbidden

from pycommon_error import validation, authorization, default

logging.basicConfig(
    format="%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.DEBUG,
)
logging.getLogger("sqlalchemy").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)


class TestErrorHandling(JSONTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config["TESTING"] = True
        api = Api(app)

        bad_request_response = validation.add_bad_request_exception_handler(api)
        unauthorized_response = authorization.add_unauthorized_exception_handler(api)
        forbidden_response = authorization.add_forbidden_exception_handler(api)
        model_not_found_response = validation.add_model_could_not_be_found_handler(api)
        validation_failed_response = validation.add_failed_validation_handler(api)
        default_response = default.add_exception_handler(api)

        @api.route("/unauthorized")
        class UnauthorizedError(Resource):
            @api.response(*unauthorized_response)
            @api.response(*default_response)
            def get(self):
                raise Unauthorized

        @api.route("/forbidden")
        class ForbiddenError(Resource):
            @api.response(*forbidden_response)
            @api.response(*default_response)
            def get(self):
                raise Forbidden

        @api.route("/bad_request")
        class BadRequestError(Resource):
            @api.response(*bad_request_response)
            @api.response(*default_response)
            def get(self):
                raise BadRequest

        @api.route("/model_not_found")
        class ModelNotFoundError(Resource):
            @api.response(*model_not_found_response)
            @api.response(*default_response)
            def get(self):
                row = {"value": "my_value1"}
                raise validation.ModelCouldNotBeFound(row)

        @api.route("/validation_failed_item")
        class ValidationFailedItemError(Resource):
            @api.response(*validation_failed_response)
            @api.response(*default_response)
            def get(self):
                received_data = {"key 1": "value 1", "key 2": 1}
                errors = {
                    "a field": ["an error"],
                    "another_field": ["first error", "second error"],
                }
                raise validation.ValidationFailed(received_data, errors=errors)

        @api.route("/validation_failed_list")
        class ValidationFailedListError(Resource):
            @api.response(*validation_failed_response)
            @api.response(*default_response)
            def get(self):
                received_data = [
                    {"key 1": "value 1", "key 2": 1},
                    {"key 1": "value 2", "key 2": 2},
                ]
                errors = {
                    0: {"a field": ["an error 1."]},
                    1: {
                        "a field": ["an error 2."],
                        "another_field": ["first error 2", "second error 2"],
                    },
                }
                raise validation.ValidationFailed(received_data, errors=errors)

        @api.route("/default_error")
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
        response = self.client.get("/unauthorized")
        self.assert401(response)
        self.assert_json(
            response,
            {
                "message": "401 Unauthorized: The server could not verify that you are authorized to access the URL "
                "requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser "
                "doesn't understand how to supply the credentials required."
            },
        )

    def test_forbidden(self):
        response = self.client.get("/forbidden")
        self.assert403(response)
        self.assert_json(
            response,
            {
                "message": "403 Forbidden: You don't have the permission to access the requested resource. It is either "
                "read-protected or not readable by the server."
            },
        )

    def test_bad_request(self):
        response = self.client.get("/bad_request")
        self.assert400(response)
        self.assert_json(
            response,
            {
                "message": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
            },
        )

    def test_model_not_found(self):
        response = self.client.get("/model_not_found")
        self.assert404(response)
        self.assert_json(
            response,
            {
                "message": "Corresponding model could not be found. You have requested this URI [/model_not_found] but "
                "did you mean /model_not_found ?"
            },
        )

    def test_default(self):
        response = self.client.get("/default_error")
        self.assert500(response)
        self.assert_json(response, {"message": ""})

    def test_validation_failed_item(self):
        response = self.client.get("/validation_failed_item")
        self.assert400(response)
        self.assert_json(
            response,
            {
                "fields": [
                    {"item": 1, "field_name": "a field", "messages": ["an error"]},
                    {
                        "item": 1,
                        "field_name": "another_field",
                        "messages": ["first error", "second error"],
                    },
                ],
                "message": "Errors: {'a field': ['an error'], 'another_field': ['first error', 'second error']}\n"
                "Received: {'key 1': 'value 1', 'key 2': 1}",
            },
        )

    def test_validation_failed_list(self):
        response = self.client.get("/validation_failed_list")
        self.assert400(response)
        self.assert_json(
            response,
            {
                "fields": [
                    {"item": 1, "field_name": "a field", "messages": ["an error 1."]},
                    {"item": 2, "field_name": "a field", "messages": ["an error 2."]},
                    {
                        "item": 2,
                        "field_name": "another_field",
                        "messages": ["first error 2", "second error 2"],
                    },
                ],
                "message": "Errors: {0: {'a field': ['an error 1.']}, 1: {'a field': ['an error 2.'], 'another_field': "
                "['first error 2', 'second error 2']}}\n"
                "Received: [{'key 1': 'value 1', 'key 2': 1}, {'key 1': 'value 2', 'key 2': 2}]",
            },
        )
