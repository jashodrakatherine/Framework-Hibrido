from web.locators.dashboard import DashboardLocators
from web.pages.base_page import BasePage


class DashboardPage(BasePage):
    def is_loaded(self) -> bool:
        return self.is_visible(DashboardLocators.INVENTORY_LIST)

    def product_count(self) -> int:
        return self.page.locator(DashboardLocators.PRODUCT_TITLES).count()

    def logout(self) -> None:
        self.click(DashboardLocators.MENU_BUTTON)
        self.click(DashboardLocators.LOGOUT_LINK)
