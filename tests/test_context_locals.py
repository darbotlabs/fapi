from __future__ import annotations

from fapi import FastAPI
from fapi.context import current_app, g, request
from fapi.testclient import TestClient


def test_context_locals_set_and_reset() -> None:
    app = FastAPI(use_context_locals=True)

    @app.get("/ctx")
    def ctx_view() -> dict[str, object]:
        had_value = "value" in g
        g["value"] = "set"
        return {
            "app_title": current_app.title,
            "method": request.method,
            "had_value": had_value,
        }

    client = TestClient(app)
    first = client.get("/ctx")
    second = client.get("/ctx")

    assert first.json()["app_title"] == app.title
    assert first.json()["method"] == "GET"
    assert first.json()["had_value"] is False

    assert second.json()["had_value"] is False
