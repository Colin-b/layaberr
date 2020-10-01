import pytest
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.testclient import TestClient

import layaberr.starlette


@pytest.fixture
def client():
    app = Starlette(exception_handlers=layaberr.starlette.exception_handlers)

    @app.route("/bad_request")
    def bad_request(request):
        raise HTTPException(400)

    @app.route("/bad_request_detail")
    def bad_request(request):
        raise HTTPException(400, detail="Error message")

    @app.route("/default_error")
    def default_error(request):
        raise Exception

    return TestClient(app, raise_server_exceptions=False)


def test_bad_request(client):
    response = client.get("/bad_request")
    assert response.status_code == 400
    assert response.text == "Bad Request"


def test_bad_request_detail(client):
    response = client.get("/bad_request_detail")
    assert response.status_code == 400
    assert response.text == "Error message"


def test_default(client):
    response = client.get("/default_error")
    assert response.status_code == 500
    assert response.json() == {"message": ""}
