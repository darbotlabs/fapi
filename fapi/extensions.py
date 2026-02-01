"""Extension protocol for FAPI applications."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List

if TYPE_CHECKING:
    from fapi.applications import FastAPI


class Extension:
    """
    Base class for FAPI extensions.

    Subclasses may override any of these methods to contribute routers,
    middleware, dependencies, events, config defaults, or CLI commands to an app.
    Extensions should not store the app instance on themselves; they may be
    reused across apps.
    """

    def init_app(self, app: "FastAPI") -> None:
        """Called by the host application to initialize this extension."""

    def routers(self) -> Iterable[Any]:
        """Return an iterable of routers to register on the app."""
        return []

    def middleware(self) -> Iterable[Any]:
        """Return an iterable of middleware definitions."""
        return []

    def dependencies(self) -> Iterable[Any]:
        """Return an iterable of (depends, override) pairs."""
        return []

    def lifespan_hooks(self) -> Iterable[Callable[..., Any]]:
        """Return an iterable of callables to register on the app's lifespan."""
        return []

    def tool_metadata(self) -> List[Dict[str, Any]]:
        """Return a list of tool schemas (metadata) defined by this extension."""
        return []

    def config_defaults(self) -> Dict[str, Any]:
        """Return default configuration values for this extension."""
        return {}

    def cli_commands(self) -> Iterable[Callable[..., Any]]:
        """Return CLI command functions to register with the app CLI."""
        return []
