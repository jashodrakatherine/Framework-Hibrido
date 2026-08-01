"""Captura de screenshots y artefactos de fallo (HTML de la página)."""
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page

from shared.config.settings import PROJECT_ROOT, get_settings
from shared.core.logger import get_logger

logger = get_logger("screenshots")

_settings = get_settings()
SCREENSHOTS_DIR = PROJECT_ROOT / _settings.paths.get("screenshots", "screenshots")
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


def take_screenshot(page: Page, name: str, full_page: bool = True) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = name.replace(" ", "_")
    path = SCREENSHOTS_DIR / f"{safe_name}_{timestamp}.png"
    page.screenshot(path=str(path), full_page=full_page)
    logger.info(f"Screenshot guardado: {path}")
    return path


def take_failure_artifacts(page: Page, test_name: str) -> None:
    """Guarda screenshot + HTML de la página en el momento del fallo."""
    take_screenshot(page, f"FAILED_{test_name}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_path = SCREENSHOTS_DIR / f"FAILED_{test_name}_{timestamp}.html"
    try:
        html_path.write_text(page.content(), encoding="utf-8")
        logger.info(f"HTML de la página guardado: {html_path}")
    except Exception as exc:
        logger.warning(f"No se pudo guardar el HTML de la página: {exc}")
