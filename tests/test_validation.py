import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient

import layaberr


@pytest.fixture
def client():
    app = Starlette(exception_handlers=layaberr.exception_handlers)

    @app.route("/model_not_found")
    def model_not_found(request):
        row = {"value": "my_value1"}
        raise layaberr.ModelCouldNotBeFound(row)

    @app.route("/validation_failed_item")
    def validation_failed_item(request):
        received_data = {"key 1": "value 1", "key 2": 1}
        errors = {
            "a field": ["an error"],
            "another_field": ["first error", "second error"],
        }
        raise layaberr.ValidationFailed(received_data, errors=errors)

    @app.route("/validation_failed_list")
    def validation_failed_list(request):
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
        raise layaberr.ValidationFailed(received_data, errors=errors)

    @app.route("/validation_failed_message")
    def validation_failed_list(request):
        raise layaberr.ValidationFailed({}, message="Error message")

    return TestClient(app, raise_server_exceptions=False)


def test_model_not_found(client):
    response = client.get("/model_not_found")
    assert response.status_code == 404
    assert response.json() == {"message": "Corresponding model could not be found."}


def test_validation_failed_item(client):
    response = client.get("/validation_failed_item")
    assert response.status_code == 400
    assert response.json() == {
        "fields": [
            {"item": 1, "field_name": "a field", "messages": ["an error"]},
            {
                "item": 1,
                "field_name": "another_field",
                "messages": ["first error", "second error"],
            },
        ]
    }


def test_validation_failed_list(client):
    response = client.get("/validation_failed_list")
    assert response.status_code == 400
    assert response.json() == {
        "fields": [
            {"item": 1, "field_name": "a field", "messages": ["an error 1."]},
            {"item": 2, "field_name": "a field", "messages": ["an error 2."]},
            {
                "item": 2,
                "field_name": "another_field",
                "messages": ["first error 2", "second error 2"],
            },
        ]
    }


def test_validation_failed_message(client):
    response = client.get("/validation_failed_message")
    assert response.status_code == 400
    assert response.json() == {
        "fields": [{"field_name": "", "item": 1, "messages": ["Error message"]}]
    }
