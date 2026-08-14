from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from tests.pages.base_page import BasePage


class TasksPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        # Элементы навигации
        self.tasks_menu_item = (By.CSS_SELECTOR, "a[href='#/tasks']")

        # Текстовые поля формы
        self.title_input = (By.CSS_SELECTOR, "input[name='title']")
        self.content_input = (
            By.CSS_SELECTOR,
            "textarea[name='content'], input[name='content']",
        )

        # Выпадающие списки на форме создания
        self.status_select = (
            By.CSS_SELECTOR,
            ".ra-input-status_id div[role='combobox'],  "
            "[data-source='status_id'] div[role='combobox']",
        )
        self.assignee_select = (
            By.CSS_SELECTOR,
            ".ra-input-assignee_id div[role='combobox'],  "
            "[data-source='assignee_id'] div[role='combobox']",
        )
        self.label_select = (
            By.CSS_SELECTOR,
            ".ra-input-label_id div[role='combobox'],  "
            "[data-source='selectArray'] div[role='combobox']",
        )

        # Фильтры на экране списка задач
        self.filter_assignee = (
            By.CSS_SELECTOR,
            "[data-source='assignee_id'] div[role='combobox']",
        )
        self.filter_status = (
            By.CSS_SELECTOR,
            "[data-source='status_id'] div[role='combobox']",
        )
        self.filter_label = (
            By.CSS_SELECTOR,
            "[data-source='label_id'] div[role='combobox']",
        )

    def navigate_to_tasks(self):
        self.driver.find_element(*self.tasks_menu_item).click()

    def open_create_form(self):
        self.driver.find_element(*self.common_create_button).click()

    def fill_task_form(self, title, status_text, assignee_text, label=None, content=None):
        actions = ActionChains(self.driver)

        title_field = self.driver.find_element(*self.title_input)
        actions.move_to_element(title_field).click().click().click().perform()
        title_field.send_keys(Keys.BACKSPACE)
        title_field.send_keys(title)

        if content:
            content_field = self.driver.find_element(*self.content_input)
            actions.move_to_element(content_field).click().click().click().perform()
            content_field.send_keys(Keys.BACKSPACE)
            content_field.send_keys(content)

        if label:
            self.wait.until(EC.element_to_be_clickable(self.label_select))
            self.driver.find_element(*self.label_select).click()

            li_locator = (By.XPATH, f"//li[contains(text(), '{label}')]")
            self.wait.until(EC.visibility_of_element_located(li_locator))
            self.driver.find_element(*li_locator).click()
            actions.send_keys(Keys.ESCAPE).perform()

        self.wait.until(EC.element_to_be_clickable(self.status_select))
        self.driver.find_element(*self.status_select).click()
        status_locator = (By.XPATH, f"//li[contains(text(), '{status_text}')]")
        self.wait.until(EC.visibility_of_element_located(status_locator))
        self.driver.find_element(*status_locator).click()

        self.wait.until(EC.element_to_be_clickable(self.assignee_select))
        self.driver.find_element(*self.assignee_select).click()
        assignee_locator = (By.XPATH, f"//li[contains(text(), '{assignee_text}')]")
        self.wait.until(EC.visibility_of_element_located(assignee_locator))
        self.driver.find_element(*assignee_locator).click()

    def save(self):
        self.driver.find_element(*self.common_save_button).click()

    def is_task_in_list(self, task_info):
        return self.is_text_present_in_list(task_info)

    def get_tasks_count(self):
        cards = self.driver.find_elements(By.CSS_SELECTOR, ".MuiCard-root")
        return len(cards)

    def is_task_in_column(self, task_info, column_name):
        locator = (
            f"//div[./*[contains(text(), '{column_name}')]]"
            f"//div[.//*[text()='{task_info}']]"
        )
        elements = self.driver.find_elements(By.XPATH, locator)
        return len(elements) > 0

    def open_task_edit_form(self, task_info):
        card_xpath = (
            f"//div[contains(@class, 'MuiCard-root') and .//*[text()='{task_info}']]"
        )
        card = self.driver.find_element(By.XPATH, card_xpath)
        card.find_element(*self.common_edit_button).click()

    def get_task_form_values(self):
        return {
            "title": self.driver.find_element(*self.title_input).get_attribute("value")
        }

    def change_task_status_via_edit(self, task_info, new_status_text):
        self.open_task_edit_form(task_info=task_info)
        self.driver.find_element(*self.status_select).click()
        self.driver.find_element(
            By.XPATH, f"//li[contains(text(), '{new_status_text}')]"
        ).click()
        self.save()

    def apply_status_filter(self, status_text):
        self.driver.find_element(*self.filter_status).click()
        self.driver.find_element(
            By.XPATH, f"//li[contains(text(), '{status_text}')]"
        ).click()

    def apply_assignee_filter(self, assignee_text):
        self.driver.find_element(*self.filter_assignee).click()
        self.driver.find_element(
            By.XPATH, f"//li[contains(text(), '{assignee_text}')]"
        ).click()

    def apply_label_filter(self, label_text):
        self.driver.find_element(*self.filter_label).click()
        self.driver.find_element(
            By.XPATH, f"//li[contains(text(), '{label_text}')]"
        ).click()

    def delete_task(self, task_info):
        self.open_task_edit_form(task_info=task_info)
        self.driver.find_element(*self.common_delete_selected_button).click()

    def create_new_task_shortcut(
        self, title, status_text, assignee_text, label=None, content=None
    ):
        self.open_create_form()
        self.fill_task_form(
            title=title,
            content=content,
            status_text=status_text,
            assignee_text=assignee_text,
            label=label,
        )
        self.save()
        self.navigate_to_tasks()
