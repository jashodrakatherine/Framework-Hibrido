"""Nombrado json_utils (no json.py) para no chocar con el módulo estándar `json`."""
import json
from pathlib import Path
from typing import Any, Union


def read_json(path: Union[str, Path]) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Union[str, Path], data: Any, indent: int = 2) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)
