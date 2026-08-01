"""Esperas inteligentes sobre locators de Playwright. Nunca usar time.sleep()."""
from typing import Optional

from playwright.sync_api import Locator, expect

from shared.core.logger import get_logger

logger = get_logger("waits")


def wait_for_visible(locator: Locator, timeout: Optional[int] = None) -> None:
    expect(locator).to_be_visible(timeout=timeout)


def wait_for_hidden(locator: Locator, timeout: Optional[int] = None) -> None:
    expect(locator).to_be_hidden(timeout=timeout)


def wait_for_enabled(locator: Locator, timeout: Optional[int] = None) -> None:
    expect(locator).to_be_enabled(timeout=timeout)


def wait_for_text(locator: Locator, text: str, timeout: Optional[int] = None) -> None:
    expect(locator).to_contain_text(text, timeout=timeout)


def wait_for_count(locator: Locator, count: int, timeout: Optional[int] = None) -> None:
    expect(locator).to_have_count(count, timeout=timeout)
