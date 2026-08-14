from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.pages.base_page import BasePage


class LabelsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Элементы навигации
        self.labels_menu_item = (By.CSS_SELECTOR, "a[href='#/labels']")

        # Поля формы
        self.name_input = (By.CSS_SELECTOR, "input[name='name']")

        # Уникальные заголовки колонок таблицы
        self.header_name = (By.CSS_SELECTOR, "th.column-name")

    def navigate_to_labels(self):
        self.driver.find_element(*self.labels_menu_item).click()

    def open_create_form(self):
        self.driver.find_element(*self.common_create_button).click()

    def fill_label_form(self, name):
        actions = ActionChains(self.driver)
        name_field = self.driver.find_element(*self.name_input)
        actions.move_to_element(name_field).click().click().click().perform()
        name_field.send_keys(Keys.BACKSPACE + name)

    def save(self):
        self.driver.find_element(*self.common_save_button).click()

    def is_label_in_list(self, label_info):
        return self.is_text_present_in_list(label_info)

    def open_label_edit_form(self, label_info):
        self.driver.find_element(By.XPATH, f"//*[text()='{label_info}']").click()
        self.driver.find_element(*self.common_show_button).click()
        self.driver.find_element(*self.common_edit_button).click()

    def get_label_form_values(self):
        return {"name": self.driver.find_element(*self.name_input).get_attribute("value")}

    def select_label_in_list(self, label_info):
        self.select_row_by_text(label_info)

    def delete_selected_label(self):
        self.driver.find_element(*self.common_delete_selected_button).click()

    def are_table_headers_visible(self):
        return (
            self.driver.find_element(*self.common_header_id).is_displayed()
            and self.driver.find_element(*self.header_name).is_displayed()
            and self.driver.find_element(*self.common_header_created_at).is_displayed()
        )

    def create_new_label(self, name):
        self.open_create_form()
        self.fill_label_form(name=name)
        self.save()
        self.navigate_to_labels()
