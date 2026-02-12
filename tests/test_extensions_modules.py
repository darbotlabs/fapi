from __future__ import annotations

from typing import List

import typer
from typer.testing import CliRunner

from fapi import APIRouter, Depends, FastAPI
from fapi.extensions import Extension
from fapi.modules import Module
from fapi.testclient import TestClient


def base_dep() -> str:
    return "base"


def override_dep() -> str:
    return "override"


class HeaderMiddleware:
    def __init__(self, app, header_name: str, header_value: str) -> None:
        self.app = app
        self.header_name = header_name
        self.header_value = header_value

    async def __call__(self, scope, receive, send) -> None:
        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append(
                    (self.header_name.encode(), self.header_value.encode())
                )
            await send(message)

        await self.app(scope, receive, send_wrapper)


class SampleExtension(Extension):
    def __init__(self, call_log: List[str]) -> None:
        self.call_log = call_log

    def init_app(self, app: FastAPI) -> None:
        self.call_log.append("init")

    def routers(self):
        router = APIRouter()

        @router.get("/ext")
        def ext_route(value: str = Depends(base_dep)) -> dict[str, str]:
            return {"value": value}

        return [router]

    def middleware(self):
        return [
            (HeaderMiddleware, {"header_name": "x-ext", "header_value": "enabled"})
        ]

    def dependencies(self):
        return [(base_dep, override_dep)]

    def lifespan_hooks(self):
        def startup() -> None:
            self.call_log.append("startup")

        return [startup]

    def tool_metadata(self):
        return [
            {
                "name": "ext_tool",
                "version": "1.0",
                "description": "Extension tool",
                "input_schema": {"type": "object"},
                "output_schema": {"type": "object"},
            }
        ]

    def config_defaults(self):
        return {"enabled": True}

    def cli_commands(self):
        def ext_command() -> None:
            typer.echo("extension command")

        return [ext_command]


def test_extension_registration() -> None:
    call_log: List[str] = []
    extension = SampleExtension(call_log)
    app = FastAPI(extensions=[extension])

    client = TestClient(app)
    response = client.get("/ext")

    assert response.json() == {"value": "override"}
    assert response.headers["x-ext"] == "enabled"
    assert "init" in call_log

    assert app.config.get("SAMPLEEXTENSION__ENABLED") is True
    assert app.tool_registry[0]["name"] == "ext_tool"

    runner = CliRunner()
    result = runner.invoke(app.cli_app, ["ext-command"])
    assert result.exit_code == 0
    assert "extension command" in result.output


def test_module_registration() -> None:
    module = Module("tools", prefix="/mod", tags=["mod"])
    router = APIRouter()

    @router.get("/ping")
    def ping() -> dict[str, str]:
        return {"ok": "true"}

    module.add_router(router)
    module.add_middleware(
        (HeaderMiddleware, {"header_name": "x-mod", "header_value": "on"})
    )
    module.add_config_defaults({"flag": "enabled"})
    module.add_tool_metadata(
        {
            "name": "mod_tool",
            "version": "1.0",
            "description": "Module tool",
            "input_schema": {"type": "object"},
            "output_schema": {"type": "object"},
        }
    )

    def module_command() -> None:
        typer.echo("module command")

    module.add_cli_command(module_command)

    app = FastAPI()
    app.register_module(module)

    client = TestClient(app)
    response = client.get("/mod/ping")

    assert response.json() == {"ok": "true"}
    assert response.headers["x-mod"] == "on"
    assert app.config.get("TOOLS__FLAG") == "enabled"
    assert app.tool_registry[0]["name"] == "mod_tool"

    runner = CliRunner()
    result = runner.invoke(app.cli_app, ["module-command"])
    assert result.exit_code == 0
    assert "module command" in result.output
