"""Blueprint-style module support for FAPI applications."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional

from fapi.routing import APIRouter

from fapi.events import emit

if TYPE_CHECKING:
    from fapi.applications import FastAPI


class Module:
    """
    Encapsulates a set of routes, middleware, config, hooks, and tool schemas.

    Modules defer registering these operations until attach() is called.
    """

    def __init__(self, name: str, *, prefix: str = "", tags: Optional[List[str]] = None):
        self.name = name
        self.prefix = prefix
        self.tags = tags or []
        self._operations: List[Callable[["FastAPI"], None]] = []
        self._tool_metadata: List[Dict[str, Any]] = []
        self._config_defaults: Dict[str, Any] = {}
        self._cli_commands: List[Callable[..., Any]] = []

    def add_router(self, router: APIRouter, **kwargs: Any) -> None:
        """Record a router to be included when this module attaches to an app."""

        def op(app: "FastAPI") -> None:
            app.include_router(router, prefix=self.prefix, tags=self.tags, **kwargs)

        self._operations.append(op)

    def add_middleware(self, middleware_def: Any) -> None:
        """Record middleware to add later."""

        def op(app: "FastAPI") -> None:
            app.apply_middleware_definition(middleware_def)

        self._operations.append(op)

    def add_config_defaults(self, defaults: Dict[str, Any]) -> None:
        """Record config defaults to apply when attaching."""
        self._config_defaults.update(defaults)

    def add_tool_metadata(self, schema: Dict[str, Any]) -> None:
        """Record tool metadata to register on the app."""
        self._tool_metadata.append(schema)

    def add_cli_command(self, command: Callable[..., Any]) -> None:
        """Record a CLI command to register on attach."""
        self._cli_commands.append(command)

    def add_hook(self, hook: Callable[..., Any]) -> None:
        """Record a module-specific startup hook."""

        def op(app: "FastAPI") -> None:
            app.add_event_handler("startup", hook)

        self._operations.append(op)

    def attach(self, app: "FastAPI") -> None:
        """Apply recorded operations to an app."""
        app.config.load_defaults(self._config_defaults, namespace=self.name)
        for op in self._operations:
            op(app)
        for schema in self._tool_metadata:
            app.tool_registry.append(schema)
        for command in self._cli_commands:
            app.cli_app.command()(command)
        emit("module_attached", module=self, app=app)
