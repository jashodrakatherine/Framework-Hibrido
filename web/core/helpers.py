"""Helpers reutilizables sobre Page/Locator que no encajan en BasePage."""
from pathlib import Path
from typing import List, Optional

from playwright.sync_api import Download, FrameLocator, Locator, Page

from shared.core.logger import get_logger

logger = get_logger("helpers")


def click_js(locator: Locator) -> None:
    """Click vía JS, útil cuando un overlay bloquea el click nativo."""
    locator.evaluate("el => el.click()")


def scroll_into_view(locator: Locator) -> None:
    locator.scroll_into_view_if_needed()


def drag_and_drop(source: Locator, target: Locator) -> None:
    source.drag_to(target)


def upload_file(locator: Locator, file_path: str) -> None:
    locator.set_input_files(file_path)
    logger.info(f"Archivo subido: {file_path}")


def download_file(page: Page, trigger: Locator, destination_dir: str) -> Path:
    with page.expect_download() as download_info:
        trigger.click()
    download: Download = download_info.value

    destination_path = Path(destination_dir)
    destination_path.mkdir(parents=True, exist_ok=True)
    destination = destination_path / download.suggested_filename
    download.save_as(str(destination))
    logger.info(f"Archivo descargado: {destination}")
    return destination


def switch_to_new_tab(page: Page, trigger: Locator) -> Page:
    with page.context.expect_page() as new_page_info:
        trigger.click()
    new_page = new_page_info.value
    new_page.wait_for_load_state()
    logger.info(f"Nueva pestaña abierta: {new_page.url}")
    return new_page


def get_iframe(page: Page, selector: str) -> FrameLocator:
    return page.frame_locator(selector)


def handle_next_dialog(page: Page, accept: bool = True, prompt_text: Optional[str] = None) -> None:
    """Registra un handler de un solo uso para el próximo alert/confirm/prompt."""

    def _handler(dialog):
        logger.info(f"Diálogo detectado: {dialog.type} - {dialog.message}")
        if accept:
            dialog.accept(prompt_text) if prompt_text else dialog.accept()
        else:
            dialog.dismiss()

    page.once("dialog", _handler)


def get_cookies(page: Page) -> List[dict]:
    return page.context.cookies()


def add_cookies(page: Page, cookies: List[dict]) -> None:
    page.context.add_cookies(cookies)
