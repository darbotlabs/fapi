"""Typer-based command line interface for FAPI."""
from __future__ import annotations

from typing import Optional

import typer

from fapi.factory import create_app

app_cli = typer.Typer(help="FAPI command line interface")


@app_cli.command()
def run(host: str = "127.0.0.1", port: int = 8000, reload: bool = False) -> None:
    """Run a FAPI app using uvicorn."""
    import uvicorn

    app = create_app()
    uvicorn.run(app, host=host, port=port, reload=reload)


@app_cli.command()
def list_tools() -> None:
    """List registered tool schemas."""
    app = create_app()
    for schema in getattr(app, "tool_registry", []):
        typer.echo(f"{schema.get('name')} - v{schema.get('version')}")


@app_cli.command()
def show_config(prefix: Optional[str] = None) -> None:
    """Print the effective configuration."""
    app = create_app()
    for key, value in app.config._data.items():
        if prefix and not key.startswith(prefix.upper()):
            continue
        typer.echo(f"{key} = {value}")


def main() -> None:
    """Entry point for the fapi command."""
    app_cli()
