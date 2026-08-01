from web.locators.login import LoginLocators
from web.pages.base_page import BasePage


class LoginPage(BasePage):
    def open_login(self) -> None:
        self.open("/")

    def login(self, username: str, password: str) -> None:
        self.fill(LoginLocators.USERNAME_INPUT, username)
        self.fill(LoginLocators.PASSWORD_INPUT, password)
        self.click(LoginLocators.LOGIN_BUTTON)

    def has_error(self) -> bool:
        return self.is_visible(LoginLocators.ERROR_MESSAGE)

    def get_error_message(self) -> str:
        return self.text(LoginLocators.ERROR_MESSAGE)
