import os

import pytest
from selenium import webdriver

from tests.pages.dashboard_page import DashboardPage
from tests.pages.label_page import LabelsPage
from tests.pages.login_page import LoginPage
from tests.pages.statuses_page import StatusesPage
from tests.pages.task_page import TasksPage
from tests.pages.user_page import UsersPage


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if os.path.exists("/.dockerenv") or os.path.exists("/run/secrets"):
        options.binary_location = "/usr/bin/chromium"
    else:
        pass

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(0)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def logged_in_dashboard(driver):
    base_url = os.getenv("APP_BASE_URL")
    if not base_url:
        if os.path.exists("/.dockerenv") or os.path.exists("/run/secrets"):
            base_url = "http://server:80"
        else:
            base_url = "http://localhost:5173"

    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.navigate(base_url)
    login_page.login("test_user", "correct_password")

    return dashboard_page


@pytest.fixture(scope="function")
def users_page_setup(logged_in_dashboard):
    driver = logged_in_dashboard.driver
    users_page = UsersPage(driver)
    users_page.navigate_to_users()
    return users_page


@pytest.fixture(scope="function")
def statuses_page_setup(logged_in_dashboard):
    driver = logged_in_dashboard.driver
    statuses_page = StatusesPage(driver)
    statuses_page.navigate_to_statuses()
    return statuses_page


@pytest.fixture(scope="function")
def labels_page_setup(logged_in_dashboard):
    driver = logged_in_dashboard.driver
    labels_page = LabelsPage(driver)
    labels_page.navigate_to_labels()
    return labels_page


@pytest.fixture(scope="function")
def tasks_page_setup(logged_in_dashboard):
    driver = logged_in_dashboard.driver
    tasks_page = TasksPage(driver)
    tasks_page.navigate_to_tasks()
    return tasks_page
