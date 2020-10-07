import http

import pytest
from flask import Flask
from flask_restx import Resource, Api

import layaberr.flask_restx


@pytest.fixture
def app():
    application = Flask(__name__)
    application.testing = True
    application.config["PROPAGATE_EXCEPTIONS"] = False
    application.config["ERROR_INCLUDE_MESSAGE"] = False
    api = Api(application)

    class CustomException(Exception):
        pass

    custom_response = layaberr.flask_restx.add_error_handler(
        api, CustomException, http.HTTPStatus.SERVICE_UNAVAILABLE
    )

    @api.route("/custom")
    @api.response(*custom_response)
    class Custom(Resource):
        def get(self):
            raise CustomException("This is the error")

    return application


def test_custom_exception(client):
    response = client.get("/custom")
    assert response.status_code == 503
    assert response.json == "This is the error"


def test_open_api_definition(client):
    response = client.get("/swagger.json")
    assert response.json == {
        "basePath": "/",
        "consumes": ["application/json"],
        "info": {"title": "API", "version": "1.0"},
        "paths": {
            "/custom": {
                "get": {
                    "operationId": "get_custom",
                    "responses": {
                        "503": {
                            "description": "The "
                            "server "
                            "cannot "
                            "process "
                            "the "
                            "request "
                            "due to a "
                            "high load",
                            "schema": {"type": "string"},
                        }
                    },
                    "tags": ["default"],
                }
            }
        },
        "produces": ["application/json"],
        "responses": {
            "CustomException": {"schema": {"type": "string"}},
            "MaskError": {"description": "When any error occurs on mask"},
            "ParseError": {"description": "When a mask can't be parsed"},
        },
        "swagger": "2.0",
        "tags": [{"description": "Default namespace", "name": "default"}],
    }


def test_validation_failed_str():
    assert (
        str(
            layaberr.flask_restx.ValidationFailed(
                {"field": "value"}, {"field": ["first error"]}
            )
        )
        == """Errors: {'field': ['first error']}\nReceived: {'field': 'value'}"""
    )
