from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from tests.pages.base_page import BasePage


class UsersPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Элементы навигации
        self.users_menu_item = (By.CSS_SELECTOR, "a[href='#/users']")

        # Уникальные локаторы заголовков колонок таблицы
        self.header_email = (By.CSS_SELECTOR, "th.column-email")
        self.header_first_name = (By.CSS_SELECTOR, "th.column-firstName")
        self.header_last_name = (By.CSS_SELECTOR, "th.column-lastName")

        # Поля формы
        self.email_input = (By.CSS_SELECTOR, "input[name='email']")
        self.first_name_input = (By.CSS_SELECTOR, "input[name='firstName']")
        self.last_name_input = (By.CSS_SELECTOR, "input[name='lastName']")

        # Локаторы валидации ошибок
        self.email_format_error = (
            By.XPATH,
            "//*[contains(text(), 'Incorrect email format')]",
        )
        self.required_field_error = (By.XPATH, "//*[contains(text(), 'Required')]")

    def navigate_to_users(self):
        self.driver.find_element(*self.users_menu_item).click()

    def are_table_headers_visible(self):
        return (
            self.driver.find_element(*self.common_header_id).is_displayed()
            and self.driver.find_element(*self.header_email).is_displayed()
            and self.driver.find_element(*self.header_first_name).is_displayed()
            and self.driver.find_element(*self.header_last_name).is_displayed()
            and self.driver.find_element(*self.common_header_created_at).is_displayed()
        )

    def open_create_form(self):
        self.driver.find_element(*self.common_create_button).click()

    def fill_user_form(self, email, first_name, last_name):
        actions = ActionChains(self.driver)

        email_field = self.driver.find_element(*self.email_input)
        actions.move_to_element(email_field).click().click().click().perform()
        email_field.send_keys(Keys.BACKSPACE)
        email_field.send_keys(email)

        fn_field = self.driver.find_element(*self.first_name_input)
        actions.move_to_element(fn_field).click().click().click().perform()
        fn_field.send_keys(Keys.BACKSPACE)
        fn_field.send_keys(first_name)

        ln_field = self.driver.find_element(*self.last_name_input)
        actions.move_to_element(ln_field).click().click().click().perform()
        ln_field.send_keys(Keys.BACKSPACE)
        ln_field.send_keys(last_name)

    def save(self):
        self.driver.find_element(*self.common_save_button).click()

    def create_new_user(self, email, first_name, last_name):
        self.open_create_form()
        self.fill_user_form(email, first_name, last_name)
        self.save()
        self.navigate_to_users()

    def is_user_in_list(self, user_info):
        return self.is_text_present_in_list(user_info)

    def open_edit_form(self, user_info):
        self.driver.find_element(By.XPATH, f"//*[text()='{user_info}']").click()
        self.driver.find_element(*self.common_show_button).click()
        self.driver.find_element(*self.common_edit_button).click()

    def get_form_values(self):
        return {
            "email": self.driver.find_element(*self.email_input).get_attribute("value"),
            "first_name": self.driver.find_element(*self.first_name_input).get_attribute(
                "value"
            ),
            "last_name": self.driver.find_element(*self.last_name_input).get_attribute(
                "value"
            ),
        }

    def select_all_users(self):
        self.driver.find_element(*self.common_select_all_checkbox).click()

    def select_user_in_list(self, user_info):
        self.select_row_by_text(user_info)

    def delete_selected_user(self):
        self.driver.find_element(*self.common_delete_selected_button).click()

    def is_email_validation_error_visible(self):
        return self.is_element_visible_safely(self.email_format_error)

    def is_required_error_visible(self):
        return self.is_element_visible_safely(self.required_field_error)
