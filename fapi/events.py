"""Event bus utilities for FAPI applications."""
from __future__ import annotations

from typing import (
    Any,
    AsyncIterable,
    AsyncIterator,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
)

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

EVENT_NAMES: List[str] = [
    "request_started",
    "request_finished",
    "tool_invoked",
    "tool_stream_chunk",
    "tool_completed",
    "auth_resolved",
    "exception_raised",
    "module_attached",
    "extension_registered",
]

_listeners: Dict[str, List[Callable[..., None]]] = {}


def on(event_name: str, listener: Callable[..., None]) -> None:
    """Register a listener for an event. Listeners must accept **kwargs."""
    _listeners.setdefault(event_name, []).append(listener)


def emit(event_name: str, **data: Any) -> None:
    """Emit an event to all subscribed listeners."""
    for listener in _listeners.get(event_name, []):
        try:
            listener(**data)
        except Exception:
            pass


class EventMiddleware(BaseHTTPMiddleware):
    """Emit request lifecycle events for HTTP requests."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        emit("request_started", request=request)
        response = await call_next(request)
        emit("request_finished", response=response)
        return response


def stream_with_events(tool_name: str, chunks: Iterable[Any]) -> Iterable[Any]:
    """Yield chunks while emitting tool stream events."""
    emit("tool_invoked", tool=tool_name)
    for chunk in chunks:
        emit("tool_stream_chunk", chunk=chunk, tool=tool_name)
        yield chunk
    emit("tool_completed", tool=tool_name)


async def async_stream_with_events(
    tool_name: str, chunks: AsyncIterable[Any]
) -> AsyncIterator[Any]:
    """Yield async chunks while emitting tool stream events."""
    emit("tool_invoked", tool=tool_name)
    async for chunk in chunks:
        emit("tool_stream_chunk", chunk=chunk, tool=tool_name)
        yield chunk
    emit("tool_completed", tool=tool_name)
