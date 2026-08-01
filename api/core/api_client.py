"""ApiClient: cliente HTTP reutilizable sobre `requests`, configurado vía config/*.yaml.

Igual que con Playwright (`web/core/browser.py`), un test nunca llama a
`requests` directamente: siempre pasa por `ApiClient`.
"""
from typing import Optional

import requests

from shared.config.settings import Settings, get_settings
from shared.core.logger import get_logger

logger = get_logger("api_client")


class ApiClient:
    def __init__(self, settings: Optional[Settings] = None, base_url: Optional[str] = None):
        self.settings = settings or get_settings()
        self.base_url = (base_url or self.settings.api_base_url).rstrip("/")
        self.timeout = self.settings.api.get("timeout", 15)
        self.session = requests.Session()

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        return self._request("POST", path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        return self._request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        return self._request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = self._url(path)
        kwargs.setdefault("timeout", self.timeout)

        logger.info(f"{method} {url}")
        response = self.session.request(method, url, **kwargs)
        logger.debug(f"-> {response.status_code} ({len(response.content)} bytes)")

        return response
