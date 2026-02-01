from __future__ import annotations

import importlib

from typer.testing import CliRunner

from fapi import FastAPI
from fapi import cli as app_cli

cli_module = importlib.import_module("fapi.cli")


def test_cli_list_tools(monkeypatch) -> None:
    app = FastAPI()
    app.tool_registry.append(
        {"name": "tool", "version": "1.0", "description": "tool"}
    )

    monkeypatch.setattr(cli_module, "create_app", lambda: app)

    runner = CliRunner()
    result = runner.invoke(app_cli, ["list-tools"])

    assert result.exit_code == 0
    assert "tool - v1.0" in result.output


def test_cli_show_config(monkeypatch) -> None:
    app = FastAPI(config={"mode": "dev"})
    monkeypatch.setattr(cli_module, "create_app", lambda: app)

    runner = CliRunner()
    result = runner.invoke(app_cli, ["show-config", "--prefix", "APP__"])

    assert result.exit_code == 0
    assert "APP__MODE = dev" in result.output
