from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        # Единое явное ожидание для всех страниц
        self.wait = WebDriverWait(self.driver, 4)

        # Общие кнопки для всех списков/таблиц
        self.common_create_button = (By.CSS_SELECTOR, "a[href$='/create']")
        self.common_save_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.common_show_button = (By.CSS_SELECTOR, "a[aria-label='Show']")
        self.common_edit_button = (By.CSS_SELECTOR, "a[aria-label='Edit']")

        # Элементы массовых действий в таблицах
        self.common_select_all_checkbox = (
            By.CSS_SELECTOR,
            "input[aria-label='Select all']",
        )
        self.common_row_checkbox = (By.CSS_SELECTOR, "[aria-label='Select this row']")
        self.common_delete_selected_button = (
            By.CSS_SELECTOR,
            "button[aria-label='Delete']",
        )

        # Базовые заголовки таблиц
        self.common_header_id = (By.CSS_SELECTOR, "th.column-id")
        self.common_header_created_at = (By.CSS_SELECTOR, "th.column-createdAt")

    def navigate(self, url):
        self.driver.get(url)

    def is_text_present_in_list(self, text):
        elements = self.driver.find_elements(By.XPATH, f"//*[text()='{text}']")
        return any(el.is_displayed() for el in elements)

    def get_table_rows_count(self):
        return len(self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr"))

    def select_row_by_text(self, text):
        row = self.driver.find_element(By.XPATH, f"//tr[.//text()='{text}']")
        row.find_element(By.CSS_SELECTOR, "[aria-label='Select this row']").click()

    def wait_for_text_to_disappear(self, text):
        locator = (By.XPATH, f"//*[text()='{text}']")
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            pass

    def is_element_visible_safely(self, locator):
        try:
            short_wait = WebDriverWait(self.driver, 1)
            element = short_wait.until(EC.visibility_of_element_located(locator))
            return element.is_displayed()
        except (WebDriverException, TimeoutException):
            return False
