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

    bad_request_response = layaberr.flask_restx.add_bad_request_exception_handler(api)
    unauthorized_response = layaberr.flask_restx.add_unauthorized_exception_handler(api)
    forbidden_response = layaberr.flask_restx.add_forbidden_exception_handler(api)
    validation_failed_response = layaberr.flask_restx.add_failed_validation_handler(api)
    default_response = layaberr.flask_restx.add_exception_handler(api)

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
            raise layaberr.flask_restx.ValidationFailed(received_data, errors=errors)

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
            raise layaberr.flask_restx.ValidationFailed(received_data, errors=errors)

    @api.route("/default_error")
    class DefaultError(Resource):
        @api.response(*bad_request_response)
        @api.response(*validation_failed_response)
        @api.response(*unauthorized_response)
        @api.response(*default_response)
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


def test_open_api_definition(client):
    response = client.get("/swagger.json")
    assert response.json == {
        "swagger": "2.0",
        "basePath": "/",
        "paths": {
            "/bad_request": {
                "get": {
                    "responses": {
                        "HTTPStatus.INTERNAL_SERVER_ERROR": {
                            "description": "An unexpected error occurred.",
                            "schema": {"$ref": "#/definitions/Exception"},
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "Bad request syntax or unsupported method",
                            "schema": {"$ref": "#/definitions/BadRequest"},
                        },
                    },
                    "operationId": "get_bad_request_error",
                    "tags": ["default"],
                }
            },
            "/default_error": {
                "get": {
                    "responses": {
                        "HTTPStatus.INTERNAL_SERVER_ERROR": {
                            "description": "An unexpected error occurred.",
                            "schema": {"$ref": "#/definitions/Exception"},
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "No permission -- see authorization schemes",
                            "schema": {"$ref": "#/definitions/Unauthorized"},
                        },
                        "400": {
                            "description": "Validation failed.",
                            "schema": {"$ref": "#/definitions/ValidationFailed"},
                        },
                        "HTTPStatus.BAD_REQUEST": {
                            "description": "Bad request syntax or unsupported method",
                            "schema": {"$ref": "#/definitions/BadRequest"},
                        },
                    },
                    "operationId": "get_default_error",
                    "tags": ["default"],
                }
            },
            "/forbidden": {
                "get": {
                    "responses": {
                        "HTTPStatus.INTERNAL_SERVER_ERROR": {
                            "description": "An unexpected error occurred.",
                            "schema": {"$ref": "#/definitions/Exception"},
                        },
                        "HTTPStatus.FORBIDDEN": {
                            "description": "Request forbidden -- authorization will not help",
                            "schema": {"$ref": "#/definitions/Unauthorized"},
                        },
                    },
                    "operationId": "get_forbidden_error",
                    "tags": ["default"],
                }
            },
            "/unauthorized": {
                "get": {
                    "responses": {
                        "HTTPStatus.INTERNAL_SERVER_ERROR": {
                            "description": "An unexpected error occurred.",
                            "schema": {"$ref": "#/definitions/Exception"},
                        },
                        "HTTPStatus.UNAUTHORIZED": {
                            "description": "No permission -- see authorization schemes",
                            "schema": {"$ref": "#/definitions/Unauthorized"},
                        },
                    },
                    "operationId": "get_unauthorized_error",
                    "tags": ["default"],
                }
            },
            "/validation_failed_item": {
                "get": {
                    "responses": {
                        "HTTPStatus.INTERNAL_SERVER_ERROR": {
                            "description": "An unexpected error occurred.",
                            "schema": {"$ref": "#/definitions/Exception"},
                        },
                        "400": {
                            "description": "Validation failed.",
                            "schema": {"$ref": "#/definitions/ValidationFailed"},
                        },
                    },
                    "operationId": "get_validation_failed_item_error",
                    "tags": ["default"],
                }
            },
            "/validation_failed_list": {
                "get": {
                    "responses": {
                        "HTTPStatus.INTERNAL_SERVER_ERROR": {
                            "description": "An unexpected error occurred.",
                            "schema": {"$ref": "#/definitions/Exception"},
                        },
                        "400": {
                            "description": "Validation failed.",
                            "schema": {"$ref": "#/definitions/ValidationFailed"},
                        },
                    },
                    "operationId": "get_validation_failed_list_error",
                    "tags": ["default"],
                }
            },
        },
        "info": {"title": "API", "version": "1.0"},
        "produces": ["application/json"],
        "consumes": ["application/json"],
        "tags": [{"name": "default", "description": "Default namespace"}],
        "definitions": {
            "BadRequest": {
                "required": ["message"],
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Description of the error.",
                        "example": "This is a description of the error.",
                    }
                },
                "type": "object",
            },
            "Unauthorized": {
                "required": ["message"],
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Description of the error.",
                        "example": "This is a description of the error.",
                    }
                },
                "type": "object",
            },
            "ValidationFailed": {
                "properties": {
                    "fields": {
                        "type": "array",
                        "items": {"$ref": "#/definitions/FieldValidationFailed"},
                    }
                },
                "type": "object",
            },
            "FieldValidationFailed": {
                "required": ["field_name", "item"],
                "properties": {
                    "item": {
                        "type": "integer",
                        "description": "Position of the item that could not be validated.",
                        "example": 1,
                    },
                    "field_name": {
                        "type": "string",
                        "description": "Name of the field that could not be validated.",
                        "example": "sample_field_name",
                    },
                    "messages": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "Reason why the validation failed.",
                            "example": "This is the reason why this field was not validated.",
                        },
                    },
                },
                "type": "object",
            },
            "Exception": {
                "required": ["message"],
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Description of the error.",
                        "example": "This is a description of the error.",
                    }
                },
                "type": "object",
            },
        },
        "responses": {
            "ParseError": {"description": "When a mask can't be parsed"},
            "MaskError": {"description": "When any error occurs on mask"},
            "BadRequest": {
                "description": "This is the Bad Request error handling",
                "schema": {"$ref": "#/definitions/BadRequest"},
            },
            "Unauthorized": {
                "description": "This is the Unauthorized error handling",
                "schema": {"$ref": "#/definitions/Unauthorized"},
            },
            "Forbidden": {
                "description": "This is the Forbidden error handling",
                "schema": {"$ref": "#/definitions/Unauthorized"},
            },
            "ValidationFailed": {
                "description": "This is the default validation error handling",
                "schema": {"$ref": "#/definitions/ValidationFailed"},
            },
            "Exception": {
                "description": "This is the default error handling",
                "schema": {"$ref": "#/definitions/Exception"},
            },
        },
    }
