"""Orquesta BrowserManager + contexto + página, y maneja trace on-failure."""
from pathlib import Path
from typing import Optional

from playwright.sync_api import BrowserContext, Page

from shared.config.settings import get_settings
from web.core.browser import BrowserManager
from shared.core.logger import get_logger

logger = get_logger("playwright_manager")


class PlaywrightManager:
    def __init__(self, **browser_overrides):
        self.settings = get_settings()
        self.browser_manager = BrowserManager(self.settings, **browser_overrides)
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def start(self) -> Page:
        self.browser_manager.launch()
        self.context = self.browser_manager.new_context()
        self.page = self.context.new_page()
        logger.info(f"Nueva página creada. base_url={self.settings.base_url}")
        return self.page

    def save_trace(self, path: str, failed: bool) -> None:
        """Detiene el tracing. Guarda el archivo solo si aplica según config.recording.trace."""
        if self.context is None:
            return

        trace_mode = self.settings.recording.get("trace", "off")
        started = trace_mode in ("on", "retain-on-failure")
        if not started:
            return

        should_save = trace_mode == "on" or (trace_mode == "retain-on-failure" and failed)
        if should_save:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            self.context.tracing.stop(path=path)
            logger.info(f"Trace guardado: {path}")
        else:
            self.context.tracing.stop()

    def stop(self) -> None:
        if self.context is not None:
            self.context.close()
            self.context = None
        self.browser_manager.close()
        self.page = None
