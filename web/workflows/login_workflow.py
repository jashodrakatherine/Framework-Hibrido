"""Los Workflows representan procesos completos de negocio, no pantallas.

Un test llama a login_workflow.login(...), nunca arma el flujo paso a paso.
"""
from shared.core.exceptions import WorkflowError
from shared.core.logger import get_logger
from web.pages.dashboard_page import DashboardPage
from web.pages.login_page import LoginPage

logger = get_logger("login_workflow")


class LoginWorkflow:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)

    def login(self, username: str, password: str) -> DashboardPage:
        logger.info("Login iniciado")
        logger.info(f"Usuario: {username}")

        self.login_page.open_login()
        self.login_page.login(username, password)

        if self.login_page.has_error():
            error = self.login_page.get_error_message()
            logger.error(f"Login falló: {error}")
            raise WorkflowError(f"Login falló: {error}")

        if not self.dashboard_page.is_loaded():
            raise WorkflowError("El dashboard no cargó tras el login")

        logger.info("Dashboard cargado")
        logger.info("Proceso OK")
        return self.dashboard_page
