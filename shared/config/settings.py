"""Carga y fusiona config.yaml + config/environments/<env>.yaml.

Nunca hardcodear URLs ni credenciales en el código: todo sale de aquí.
"""
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = Path(__file__).resolve().parent
ENVIRONMENTS_DIR = CONFIG_DIR / "environments"


def _load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


class Settings:
    def __init__(self, env: Optional[str] = None):
        base = _load_yaml(CONFIG_DIR / "config.yaml")
        self.env = env or os.getenv("ENV") or base.get("default_environment", "dev")

        env_file = ENVIRONMENTS_DIR / f"{self.env}.yaml"
        if not env_file.exists():
            raise FileNotFoundError(f"No existe el archivo de entorno: {env_file}")

        env_config = _load_yaml(env_file)
        self._data = _deep_merge(base, env_config)

    def get(self, dotted_key: str, default: Any = None) -> Any:
        node: Any = self._data
        for part in dotted_key.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node

    @property
    def base_url(self) -> str:
        return self._data.get("base_url", "")

    @property
    def api_base_url(self) -> str:
        return self._data.get("api_base_url", "")

    @property
    def api(self) -> Dict[str, Any]:
        return self._data.get("api", {"timeout": 15})

    @property
    def browser(self) -> Dict[str, Any]:
        return self._data.get("browser", {})

    @property
    def viewport(self) -> Dict[str, Any]:
        return self._data.get("viewport", {"width": 1280, "height": 720})

    @property
    def recording(self) -> Dict[str, Any]:
        return self._data.get("recording", {})

    @property
    def paths(self) -> Dict[str, Any]:
        return self._data.get("paths", {})

    @property
    def retry(self) -> Dict[str, Any]:
        return self._data.get("retry", {"max_attempts": 3, "delay_seconds": 1})


_settings: Optional[Settings] = None


def get_settings(env: Optional[str] = None, reload: bool = False) -> Settings:
    global _settings
    if _settings is None or reload:
        _settings = Settings(env=env)
    return _settings
