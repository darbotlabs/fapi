import http

from fapi import FastAPI
from fapi.testclient import TestClient


def test_no_content():
    app = FastAPI()

    @app.get("/no-content", status_code=http.HTTPStatus.NO_CONTENT)
    def return_no_content() -> "None":
        return

    client = TestClient(app)
    response = client.get("/no-content")
    assert response.status_code == http.HTTPStatus.NO_CONTENT, response.text
    assert not response.content
