import os

import pytest

from tests.pages.dashboard_page import DashboardPage
from tests.pages.login_page import LoginPage

BASE_URL = os.getenv("APP_BASE_URL")
if not BASE_URL:
    if os.path.exists("/.dockerenv") or os.path.exists("/run/secrets"):
        # Внутри Docker Хекслета стучимся на caddy прокси (хост server) по порту 80
        BASE_URL = "http://server:80"
    else:
        BASE_URL = "http://localhost:5173"


@pytest.mark.smoke
def test_login_form_rendering(driver):
    login_page = LoginPage(driver)

    login_page.navigate(BASE_URL)
    assert driver.title == "Task manager", (
        f"Неверный заголовок. Ожидался 'Task manager', но получили '{driver.title}'"
    )
    assert login_page.driver.find_element(*login_page.username_input).is_displayed(), (
        "Поле ввода логина не отображается на форме"
    )
    assert login_page.driver.find_element(*login_page.password_input).is_displayed(), (
        "Поле ввода пароля не отображается на форме"
    )
    assert login_page.driver.find_element(*login_page.submit_button).is_displayed(), (
        "Кнопка Sign In  не отображается"
    )


@pytest.mark.smoke
def test_successful_login(driver):
    login_page = LoginPage(driver)
    dashboard_page = DashboardPage(driver)

    login_page.navigate(BASE_URL)
    login_page.login("admin", "admin")

    assert dashboard_page.is_board_visible(), "Дашборд не отобразился после входа"


@pytest.mark.smoke
def test_successful_logout(logged_in_dashboard):
    dashboard_page = logged_in_dashboard
    dashboard_page.logout()
    login_page = LoginPage(dashboard_page.driver)

    assert login_page.is_text_present_in_list("Sign in"), (
        "Не удалось вернуться на форму логина после выхода"
    )
