"""Example module with a router and config defaults."""
from __future__ import annotations

from fapi import FastAPI, Module
from fapi.routing import APIRouter

module = Module("metrics", prefix="/metrics", tags=["metrics"])
router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


module.add_router(router)
module.add_config_defaults({"enabled": True})


def build_app() -> FastAPI:
    app = FastAPI()
    app.register_module(module)
    return app
