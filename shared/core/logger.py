"""Logger centralizado: consola + archivo por ejecución en logs/.

Uso: logger = get_logger(__name__); logger.info("mensaje")
"""
import logging
import sys
from datetime import datetime
from pathlib import Path

from shared.config.settings import PROJECT_ROOT, get_settings

_settings = get_settings()
LOG_DIR = PROJECT_ROOT / _settings.paths.get("logs", "logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

_RUN_TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
_LOG_FILE = LOG_DIR / f"run_{_RUN_TIMESTAMP}.log"

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATEFMT = "%Y-%m-%d %H:%M:%S"

_root = logging.getLogger("automation")


def _configure_root() -> None:
    if _root.handlers:
        return
    _root.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATEFMT))

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATEFMT))

    _root.addHandler(file_handler)
    _root.addHandler(console_handler)
    _root.propagate = False


_configure_root()


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"automation.{name}")


def current_log_file() -> Path:
    return _LOG_FILE
