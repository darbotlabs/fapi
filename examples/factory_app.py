"""Example factory-based application setup."""
from __future__ import annotations

from fapi import Module, create_app
from fapi.routing import APIRouter

router = APIRouter()


@router.get("/")
def index() -> dict[str, str]:
    return {"hello": "world"}


module = Module("core")
module.add_router(router)

app = create_app(config={"log_level": "info"}, modules=[module])
