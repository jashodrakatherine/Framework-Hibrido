"""Fixtures para la suite de API."""
import pytest

from api.core.api_client import ApiClient


@pytest.fixture
def api_client():
    return ApiClient()
