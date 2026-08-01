"""Fixtures compartidas por la suite web (smoke, regression).

`page`: levanta el navegador vía PlaywrightManager, y al terminar el test
guarda screenshot/HTML/trace si falló, según config/config.yaml.
"""
from pathlib import Path

import pytest

from shared.config.settings import PROJECT_ROOT, get_settings
from shared.core.logger import get_logger
from web.core.playwright_manager import PlaywrightManager
from web.core.screenshots import take_failure_artifacts

logger = get_logger("conftest")

REPORTS_DIR = PROJECT_ROOT / get_settings().paths.get("reports", "reports")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.fixture
def page(request):
    manager = PlaywrightManager()
    pw_page = manager.start()

    yield pw_page

    call_report = getattr(request.node, "rep_call", None)
    failed = call_report is not None and call_report.failed
    test_name = request.node.name

    if failed:
        logger.error(f"Test falló: {test_name}")
        take_failure_artifacts(pw_page, test_name)

    trace_path = REPORTS_DIR / "traces" / f"{test_name}.zip"
    manager.save_trace(str(trace_path), failed=failed)
    manager.stop()
