from __future__ import annotations

from pathlib import Path

from fapi import FastAPI
from fapi.config import Config


def test_config_defaults_and_env(monkeypatch) -> None:
    config = Config()
    config.load_defaults({"value": "default"})
    monkeypatch.setenv("FAPI_VALUE", "env")
    config.from_env(prefix="FAPI_")

    assert config.get("VALUE") == "default"
    assert config.get("FAPI_VALUE") == "env"


def test_app_config_instance_folder(tmp_path: Path, monkeypatch) -> None:
    instance_path = tmp_path / "instance"
    instance_path.mkdir()
    config_file = instance_path / "config.py"
    config_file.write_text("APP_NAME = 'instance'\n", encoding="utf-8")

    monkeypatch.setenv("FAPI_ENV", "set")
    app = FastAPI(config={"setting": "value"}, instance_path=str(instance_path))

    assert app.config.get("TITLE") == "FastAPI"
    assert app.config.get("APP__SETTING") == "value"
    assert app.config.get("FAPI_ENV") == "set"
    assert app.config.get("APP_NAME") == "instance"
