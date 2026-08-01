"""BrowserManager: lanza y configura el navegador según config/*.yaml.

Soporta chromium, chrome, edge, firefox y webkit.
"""
from typing import Optional

from playwright.sync_api import Browser, BrowserContext, Playwright, sync_playwright

from shared.config.settings import PROJECT_ROOT, Settings, get_settings
from shared.core.exceptions import BrowserLaunchError
from shared.core.logger import get_logger

logger = get_logger("browser")

_ENGINE_MAP = {
    "chromium": "chromium",
    "chrome": "chromium",   # chrome/edge corren sobre el motor chromium con "channel"
    "edge": "chromium",
    "firefox": "firefox",
    "webkit": "webkit",
}

_CHANNEL_MAP = {
    "chrome": "chrome",
    "edge": "msedge",
}


class BrowserManager:
    def __init__(self, settings: Optional[Settings] = None, **overrides):
        self.settings = settings or get_settings()
        browser_cfg = dict(self.settings.browser)
        browser_cfg.update(overrides)

        self.browser_name: str = browser_cfg.get("name", "chromium")
        self.headless: bool = browser_cfg.get("headless", True)
        self.slow_mo: int = browser_cfg.get("slow_mo", 0)
        self.timeout: int = browser_cfg.get("timeout", 30000)

        if self.browser_name not in _ENGINE_MAP:
            raise BrowserLaunchError(f"Navegador no soportado: {self.browser_name}")

        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None

    def launch(self) -> Browser:
        engine_name = _ENGINE_MAP[self.browser_name]
        channel = _CHANNEL_MAP.get(self.browser_name)

        logger.info(
            f"Lanzando navegador: {self.browser_name} "
            f"(headless={self.headless}, slow_mo={self.slow_mo})"
        )

        self._playwright = sync_playwright().start()
        engine = getattr(self._playwright, engine_name)

        launch_kwargs = {"headless": self.headless, "slow_mo": self.slow_mo}
        if channel:
            launch_kwargs["channel"] = channel

        try:
            self._browser = engine.launch(**launch_kwargs)
        except Exception as exc:
            self.close()
            raise BrowserLaunchError(f"No se pudo lanzar {self.browser_name}: {exc}") from exc

        return self._browser

    def new_context(self, **kwargs) -> BrowserContext:
        if self._browser is None:
            raise BrowserLaunchError("El navegador no ha sido lanzado. Llama a launch() primero.")

        viewport = self.settings.viewport
        recording = self.settings.recording

        context_kwargs = {
            "viewport": {"width": viewport.get("width", 1280), "height": viewport.get("height", 720)},
            "base_url": self.settings.base_url,
        }

        if recording.get("video") in ("on", "retain-on-failure"):
            videos_dir = PROJECT_ROOT / self.settings.paths.get("reports", "reports") / "videos"
            context_kwargs["record_video_dir"] = str(videos_dir)

        context_kwargs.update(kwargs)
        context = self._browser.new_context(**context_kwargs)
        context.set_default_timeout(self.timeout)

        if recording.get("trace") in ("on", "retain-on-failure"):
            context.tracing.start(screenshots=True, snapshots=True, sources=True)

        return context

    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
            self._browser = None
        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
        logger.info("Navegador cerrado")
