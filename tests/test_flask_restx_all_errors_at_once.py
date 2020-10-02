import pytest
from flask import Flask
from flask_restx import Resource, Api
from werkzeug.exceptions import Unauthorized, BadRequest, Forbidden

import layaberr.flask_restx


@pytest.fixture
def app():
    application = Flask(__name__)
    application.testing = True
    application.config["PROPAGATE_EXCEPTIONS"] = False
    api = Api(application)

    error_responses = layaberr.flask_restx.add_error_handlers(api)

    @api.route("/unauthorized")
    @api.doc(**error_responses)
    class UnauthorizedError(Resource):
        def get(self):
            raise Unauthorized

    @api.route("/forbidden")
    @api.doc(**error_responses)
    class ForbiddenError(Resource):
        def get(self):
            raise Forbidden

    @api.route("/bad_request")
    @api.doc(**error_responses)
    class BadRequestError(Resource):
        def get(self):
            raise BadRequest

    @api.route("/validation_failed_item")
    @api.doc(**error_responses)
    class ValidationFailedItemError(Resource):
        def get(self):
            received_data = {"key 1": "value 1", "key 2": 1}
            errors = {
                "a field": ["an error"],
                "another_field": ["first error", "second error"],
            }
            raise layaberr.flask_restx.ValidationFailed(received_data, errors=errors)

    @api.route("/validation_failed_list")
    @api.doc(**error_responses)
    class ValidationFailedListError(Resource):
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
            raise layaberr.flask_restx.ValidationFailed(received_data, errors=errors)

    @api.route("/default_error")
    @api.doc(**error_responses)
    class DefaultError(Resource):
        def get(self):
            raise Exception

    return application


def test_unauthorized(client):
    response = client.get("/unauthorized")
    assert response.status_code == 401
    assert response.json == {
        "message": "401 Unauthorized: The server could not verify that you are authorized to access the URL "
        "requested. You either supplied the wrong credentials (e.g. a bad password), or your browser "
        "doesn't understand how to supply the credentials required."
    }


def test_forbidden(client):
    response = client.get("/forbidden")
    assert response.status_code == 403
    assert response.json == {
        "message": "403 Forbidden: You don't have the permission to access the requested resource. It is either "
        "read-protected or not readable by the server."
    }


def test_bad_request(client):
    response = client.get("/bad_request")
    assert response.status_code == 400
    assert response.json == {
        "message": "400 Bad Request: The browser (or proxy) sent a request that this server could not understand."
    }


def test_default(client):
    response = client.get("/default_error")
    assert response.status_code == 500
    assert response.json == {"message": ""}


def test_validation_failed_item(client):
    response = client.get("/validation_failed_item")
    assert response.status_code == 400
    assert response.json == {
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
    }


def test_validation_failed_list(client):
    response = client.get("/validation_failed_list")
    assert response.status_code == 400
    assert response.json == {
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
    }