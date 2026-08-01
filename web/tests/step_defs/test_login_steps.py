"""Step definitions para tests/features/login.feature.

Los steps hablan con Pages (nunca con Playwright directo), igual que el
resto del framework. LoginWorkflow sigue disponible para procesos
compuestos (ej. un checkout que necesita loguearse primero).
"""
import pytest
from pytest_bdd import given, parsers, scenarios, then, when

from web.pages.dashboard_page import DashboardPage
from web.pages.login_page import LoginPage

scenarios("login.feature")


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def dashboard_page(page):
    return DashboardPage(page)


@given("que estoy en la página de login")
def open_login_page(login_page):
    login_page.open_login()


@when(parsers.re(r'inicio sesión con el usuario "(?P<username>.*)" y la contraseña "(?P<password>.*)"'))
def do_login(login_page, username, password):
    login_page.login(username, password)


@then("debo ver el dashboard cargado")
def assert_dashboard_loaded(dashboard_page):
    assert dashboard_page.is_loaded()


@then("debo ver al menos un producto listado")
def assert_products_listed(dashboard_page):
    assert dashboard_page.product_count() > 0


@then("debo ver un error de login")
def assert_login_error(login_page):
    assert login_page.has_error()
