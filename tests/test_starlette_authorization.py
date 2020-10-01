import pytest
from starlette.applications import Starlette
from starlette.testclient import TestClient

import layaberr.starlette


@pytest.fixture
def client():
    app = Starlette(exception_handlers=layaberr.exception_handlers)

    @app.route("/unauthorized")
    def unauthorized(request):
        raise layaberr.starlette.Unauthorized

    @app.route("/unauthorized_detail")
    def unauthorized(request):
        raise layaberr.starlette.Unauthorized(detail="Error message")

    @app.route("/forbidden")
    def forbidden(request):
        raise layaberr.starlette.Forbidden

    @app.route("/forbidden_detail")
    def unauthorized(request):
        raise layaberr.starlette.Forbidden(detail="Error message")

    return TestClient(app, raise_server_exceptions=False)


def test_unauthorized(client):
    response = client.get("/unauthorized")
    assert response.status_code == 401
    assert response.json() == {"message": "No permission -- see authorization schemes"}


def test_unauthorized_detail(client):
    response = client.get("/unauthorized_detail")
    assert response.status_code == 401
    assert response.json() == {"message": "Error message"}


def test_forbidden(client):
    response = client.get("/forbidden")
    assert response.status_code == 403
    assert response.json() == {
        "message": "Request forbidden -- authorization will not help"
    }


def test_forbidden_detail(client):
    response = client.get("/forbidden_detail")
    assert response.status_code == 403
    assert response.json() == {"message": "Error message"}
