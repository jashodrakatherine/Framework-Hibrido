"""Toda Page hereda de aquí. Nunca se llama a Playwright directamente desde un test."""
from typing import Optional

from playwright.sync_api import Locator, Page

from shared.core.logger import get_logger
from web.core.screenshots import take_screenshot
from web.core.waits import wait_for_hidden, wait_for_visible

logger = get_logger("base_page")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, path: str = "") -> None:
        logger.info(f"Navegando a: {path or '/'}")
        self.page.goto(path)

    def click(self, selector: str) -> None:
        logger.debug(f"Click en: {selector}")
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        logger.debug(f"Escribiendo en: {selector}")
        self.page.locator(selector).fill(value)

    def text(self, selector: str) -> str:
        return self.page.locator(selector).text_content() or ""

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        wait_for_visible(self.page.locator(selector), timeout=timeout)

    def wait_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        wait_for_hidden(self.page.locator(selector), timeout=timeout)

    def select_option(self, selector: str, value: str) -> None:
        self.page.locator(selector).select_option(value)

    def check(self, selector: str) -> None:
        self.page.locator(selector).check()

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        return self.page.locator(selector).get_attribute(attribute)

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def screenshot(self, name: str):
        return take_screenshot(self.page, name)
