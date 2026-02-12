"""Context-local proxies for FAPI applications."""
from __future__ import annotations

import contextvars
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional

from starlette.requests import Request

if TYPE_CHECKING:
    from fapi.applications import FastAPI


class LocalProxy:
    """A minimal proxy for context-local objects."""

    def __init__(self, func: Callable[[], Any]) -> None:
        self._func = func

    def _get_current_object(self) -> Any:
        return self._func()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._get_current_object(), name)

    def __getitem__(self, key: Any) -> Any:
        return self._get_current_object()[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._get_current_object()[key] = value

    def __delitem__(self, key: Any) -> None:
        del self._get_current_object()[key]

    def __iter__(self):
        return iter(self._get_current_object())

    def __len__(self) -> int:
        return len(self._get_current_object())

    def __contains__(self, item: Any) -> bool:
        return item in self._get_current_object()

    def __repr__(self) -> str:
        return repr(self._get_current_object())


_app_ctx: contextvars.ContextVar[Optional["FastAPI"]] = contextvars.ContextVar(
    "fapi_app"
)
_req_ctx: contextvars.ContextVar[Optional[Any]] = contextvars.ContextVar("fapi_request")
_g_ctx: contextvars.ContextVar[dict] = contextvars.ContextVar("fapi_g", default={})

current_app = LocalProxy(lambda: _app_ctx.get())
request = LocalProxy(lambda: _req_ctx.get())
g = LocalProxy(lambda: _g_ctx.get())


@dataclass(frozen=True)
class Context:
    """Container for context-local proxies."""

    current_app: LocalProxy
    request: LocalProxy
    g: LocalProxy


context = Context(current_app=current_app, request=request, g=g)


class ContextMiddleware:
    """Middleware that pushes app, request and g into contextvars per request."""

    def __init__(self, app: "FastAPI", app_context: Optional["FastAPI"] = None) -> None:
        self.app = app
        self.app_context = app_context or app

    async def __call__(self, scope, receive, send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        token_app = _app_ctx.set(self.app_context)
        token_req = _req_ctx.set(Request(scope, receive=receive))
        token_g = _g_ctx.set({})
        try:
            await self.app(scope, receive, send)
        finally:
            _app_ctx.reset(token_app)
            _req_ctx.reset(token_req)
            _g_ctx.reset(token_g)
