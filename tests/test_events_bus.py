from __future__ import annotations

from typing import Any, Dict, List

from fapi import FastAPI
from fapi.events import on, stream_with_events
from fapi.testclient import TestClient


def test_request_events(monkeypatch) -> None:
    events: List[str] = []

    def record(event_name: str):
        def _listener(**_: Any) -> None:
            events.append(event_name)

        return _listener

    monkeypatch.setattr("fapi.events._listeners", {})
    on("request_started", record("request_started"))
    on("request_finished", record("request_finished"))

    app = FastAPI()

    @app.get("/ping")
    def ping() -> Dict[str, str]:
        return {"ok": "true"}

    client = TestClient(app)
    response = client.get("/ping")

    assert response.json() == {"ok": "true"}
    assert events == ["request_started", "request_finished"]


def test_stream_events_sync(monkeypatch) -> None:
    seen: List[str] = []

    def wrap(event_name: str):
        def _listener(**data: Any) -> None:
            seen.append(event_name)

        return _listener

    monkeypatch.setattr("fapi.events._listeners", {})
    on("tool_invoked", wrap("tool_invoked"))
    on("tool_stream_chunk", wrap("tool_stream_chunk"))
    on("tool_completed", wrap("tool_completed"))

    chunks = list(stream_with_events("tool", ["a", "b"]))

    assert chunks == ["a", "b"]
    assert seen == [
        "tool_invoked",
        "tool_stream_chunk",
        "tool_stream_chunk",
        "tool_completed",
    ]


def test_extension_module_events(monkeypatch) -> None:
    events: List[str] = []

    def listener(event_name: str):
        def _listener(**_: Any) -> None:
            events.append(event_name)

        return _listener

    monkeypatch.setattr("fapi.events._listeners", {})
    on("extension_registered", listener("extension_registered"))
    on("module_attached", listener("module_attached"))

    from fapi.extensions import Extension
    from fapi.modules import Module

    app = FastAPI()

    class EventExtension(Extension):
        pass

    app.register_extension(EventExtension())
    app.register_module(Module("events"))

    assert events == ["extension_registered", "module_attached"]
