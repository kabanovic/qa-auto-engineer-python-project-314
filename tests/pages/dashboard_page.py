from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class DashboardPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.profile_menu_button = (By.CSS_SELECTOR, "button[aria-label='Profile']")
        self.logout_button = (By.CSS_SELECTOR, "li.logout")
        self.dashboard = (
            By.XPATH,
            "//*[contains(text(), 'Lorem ipsum sic dolor amet')]",
        )

    def is_board_visible(self):
        return self.driver.find_element(*self.dashboard).is_displayed()

    def logout(self):
        self.driver.find_element(*self.profile_menu_button).click()
        self.driver.find_element(*self.logout_button).click()
