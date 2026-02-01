"""Example extension that registers a CLI command."""
from __future__ import annotations

import typer

from fapi import Extension, FastAPI


class StatusExtension(Extension):
    def cli_commands(self):
        def show_status() -> None:
            typer.echo("status ok")

        return [show_status]


def build_app() -> FastAPI:
    return FastAPI(extensions=[StatusExtension()])
