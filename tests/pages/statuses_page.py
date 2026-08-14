from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.pages.base_page import BasePage


class StatusesPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Элементы навигации
        self.statuses_menu_item = (By.CSS_SELECTOR, "a[href='#/task_statuses']")

        # Поля формы
        self.name_input = (By.CSS_SELECTOR, "input[name='name']")
        self.slug_input = (By.CSS_SELECTOR, "input[name='slug']")

        # Уникальные заголовки колонок таблицы
        self.header_name = (By.CSS_SELECTOR, "th.column-name")
        self.header_slug = (By.CSS_SELECTOR, "th.column-slug")

    def navigate_to_statuses(self):
        self.driver.find_element(*self.statuses_menu_item).click()

    def open_create_form(self):
        self.driver.find_element(*self.common_create_button).click()

    def fill_status_form(self, name, slug):
        actions = ActionChains(self.driver)

        name_field = self.driver.find_element(*self.name_input)
        actions.move_to_element(name_field).click().click().click().perform()
        name_field.send_keys(Keys.BACKSPACE)
        name_field.send_keys(name)

        slug_field = self.driver.find_element(*self.slug_input)
        actions.move_to_element(slug_field).click().click().click().perform()
        slug_field.send_keys(Keys.BACKSPACE)
        slug_field.send_keys(slug)

    def save(self):
        self.driver.find_element(*self.common_save_button).click()

    def create_new_status(self, name, slug):
        self.open_create_form()
        self.fill_status_form(name, slug)
        self.save()
        self.navigate_to_statuses()

    def is_status_in_list(self, status_info):
        return self.is_text_present_in_list(status_info)

    def open_status_edit_form(self, status_info):
        self.driver.find_element(By.XPATH, f"//*[text()='{status_info}']").click()
        self.driver.find_element(*self.common_show_button).click()
        self.driver.find_element(*self.common_edit_button).click()

    def get_statuses_form_values(self):
        return {
            "name": self.driver.find_element(*self.name_input).get_attribute("value"),
            "slug": self.driver.find_element(*self.slug_input).get_attribute("value"),
        }

    def select_all_statuses(self):
        self.driver.find_element(*self.common_select_all_checkbox).click()

    def select_status_in_list(self, status_info):
        self.select_row_by_text(status_info)

    def delete_selected_status(self):
        self.driver.find_element(*self.common_delete_selected_button).click()

    def are_table_headers_visible(self):
        return (
            self.driver.find_element(*self.common_header_id).is_displayed()
            and self.driver.find_element(*self.header_name).is_displayed()
            and self.driver.find_element(*self.header_slug).is_displayed()
            and self.driver.find_element(*self.common_header_created_at).is_displayed()
        )
