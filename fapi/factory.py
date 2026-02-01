"""Application factory helpers for FAPI."""
from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from fapi.applications import FastAPI
from fapi.extensions import Extension
from fapi.modules import Module


def create_app(
    config: Optional[Dict[str, Any]] = None,
    *,
    extensions: Optional[Iterable[Extension]] = None,
    modules: Optional[Iterable[Module]] = None,
    instance_path: Optional[str] = None,
) -> FastAPI:
    """Factory to create a FAPI application."""
    app = FastAPI()
    if config:
        app.config.load_defaults(config, namespace="APP")
    if instance_path:
        app.config.load_instance_folder(instance_path)
    for extension in extensions or []:
        app.register_extension(extension)
    for module in modules or []:
        app.register_module(module)
    return app
