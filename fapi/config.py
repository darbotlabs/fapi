"""Configuration registry for FAPI applications."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional


class Config:
    """A simple configuration registry with namespacing support."""

    def __init__(self) -> None:
        self._data: Dict[str, Any] = {}
        self.instance_path: Optional[str] = None

    def load_defaults(self, defaults: Dict[str, Any], namespace: str = "") -> None:
        """Merge defaults under a namespace; use double-underscore to nest."""
        for key, value in defaults.items():
            namespaced_key = (
                f"{namespace.upper()}__{key.upper()}" if namespace else key.upper()
            )
            self._data.setdefault(namespaced_key, value)

    def from_env(self, prefix: str = "") -> None:
        """Override with environment variables matching the prefix."""
        for key, value in os.environ.items():
            if prefix and not key.startswith(prefix):
                continue
            self._data[key.upper()] = value

    def from_file(self, filename: str) -> None:
        """Load config values from a JSON or Python file."""
        if filename.endswith(".json"):
            with open(filename, encoding="utf-8") as handle:
                self._data.update(json.load(handle))
        elif filename.endswith(".py"):
            data: Dict[str, Any] = {}
            with open(filename, encoding="utf-8") as handle:
                exec(handle.read(), data)
            self._data.update({k: v for k, v in data.items() if k.isupper()})

    def load_instance_folder(self, path: str) -> None:
        """Set the instance path and load config.py within it if present."""
        self.instance_path = path
        config_py = os.path.join(path, "config.py")
        if os.path.exists(config_py):
            self.from_file(config_py)

    def get(self, key: str, default: Any = None) -> Any:
        """Retrieve a configuration value, returning a default if missing."""
        return self._data.get(key.upper(), default)

    def __getitem__(self, key: str) -> Any:
        return self._data[key.upper()]
