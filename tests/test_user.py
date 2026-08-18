import pytest
from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_1_create_and_view_user(users_page_setup):
    users_page = users_page_setup
    email = "create.test@example.com"

    # Проверяем форму создания
    users_page.open_create_form()
    assert users_page.driver.find_element(
        *users_page.common_save_button
    ).is_displayed(), "Форма создания не открылась"

    # Заполняем данные нового пользователя
    users_page.fill_user_form(email=email, first_name="QA_Name", last_name="QA_Surname")
    users_page.save()

    # Проверяем отображение всех ключевых полей в списке (Просмотр списка)
    users_page.navigate_to_users()
    assert users_page.is_user_in_list(user_info=email), (
        "Новый пользователь не появился в списке"
    )


@pytest.mark.smoke
def test_2_view_users_list(users_page_setup):
    users_page = users_page_setup

    # Проверяем, что таблица загрузилась и ключевые поля отображаются
    assert users_page.are_table_headers_visible(), "Ключевые колонки не найдены в таблице"

    # Проверяем данные в таблице
    rows_count = users_page.get_table_rows_count()
    if rows_count == 0:
        users_page.create_new_user(
            email="backup.view@example.com", first_name="Backup", last_name="User"
        )
    rows = users_page.get_all_table_rows()
    assert len(rows) > 0, "Таблица загрузилась пустой, строк с пользователями нет"
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        user_data_values = [
            cell.text.strip() for cell in cells[2:] if cell.text.strip() != ""
        ]
        assert len(user_data_values) == 4, (
            f"В строке пользователя пропущены данные. "
            f"Отобразились только: {user_data_values}"
        )

        email_field_valid = any("@" in val for val in user_data_values)
        assert email_field_valid, (
            f"Ключевое поле Email отображается не верно. "
            f"Данные строки: {user_data_values}"
        )


@pytest.mark.smoke
def test_3_edit_user_and_email_validation(users_page_setup):
    users_page = users_page_setup
    initial_email = "test@example.com"
    updated_email = "edit.updated@example.com"

    # Создаем пользователя
    users_page.create_new_user(
        email=initial_email, first_name="QA_Edit", last_name="User"
    )

    # Открываем форму редактирования
    users_page.open_edit_form(user_info=initial_email)

    # Проверяем данные
    current_values = users_page.get_form_values()
    assert current_values["email"] == initial_email, (
        "В форме открылись данные чужого пользователя"
    )

    # Проверяем валидацию email
    users_page.fill_user_form(
        email="invalid-email-format", first_name="QA_Edit", last_name="User"
    )
    users_page.save()
    assert users_page.is_email_validation_error_visible(), (
        "Сообщение 'Incorrect email format' не появилось"
    )

    users_page.fill_user_form(email="", first_name="QA_Edit", last_name="User")
    users_page.save()
    assert users_page.is_required_error_visible(), (
        "Сообщение 'Required' не появилось при пустом поле Email"
    )

    # Изменяем значения на корректные
    users_page.fill_user_form(
        email=updated_email, first_name="Updated_Edit_Name", last_name="User"
    )
    users_page.save()

    # Проверяем сохранение в общем списке
    assert users_page.is_user_in_list(user_info=updated_email), (
        "Обновленный email не сохранился в списке"
    )


@pytest.mark.smoke
def test_4_delete_single_user(users_page_setup):
    users_page = users_page_setup
    delete_email = "delete.test@example.com"

    # Создаем пользователя
    users_page.create_new_user(
        email=delete_email, first_name="QA_Delete", last_name="User"
    )

    # Выделяем созданного пользователя
    users_page.select_user_in_list(user_info=delete_email)

    # Удаляем и проверяем отсутствие в общем списке
    users_page.delete_selected_user()
    users_page.wait_for_text_to_disappear(delete_email)
    assert not users_page.is_user_in_list(user_info=delete_email), (
        "Пользователь не удалился при одиночном удалении"
    )


@pytest.mark.smoke
def test_5_mass_delete_users(users_page_setup):
    users_page = users_page_setup
    target_email = "create.test@example.com"

    # Выделяем всех пользователей
    users_page.select_all_users()

    # Удаляем и проверяем отсутствие в общем списке
    users_page.delete_selected_user()
    users_page.wait_for_text_to_disappear(target_email)
    final_rows_count = users_page.get_table_rows_count()
    assert final_rows_count == 0, (
        f"Таблица не пуста после массового удаления. Осталось строк: {final_rows_count}"
    )
