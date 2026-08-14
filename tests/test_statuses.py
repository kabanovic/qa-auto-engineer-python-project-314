import pytest


@pytest.mark.smoke
def test_1_create_status(statuses_page_setup):
    statuses_page = statuses_page_setup
    name = "Новый статус"
    slug = "new-slug"

    # Проверяем открытие формы и поля
    statuses_page.open_create_form()
    assert "/create" in statuses_page.driver.current_url, (
        "URL страницы не изменился на /create"
    )
    assert statuses_page.driver.find_element(*statuses_page.name_input).is_displayed(), (
        "Поле Название не видно"
    )
    assert statuses_page.driver.find_element(*statuses_page.slug_input).is_displayed(), (
        "Поле Slug не видно"
    )

    # Заполняем и сохраняем
    statuses_page.fill_status_form(name=name, slug=slug)
    statuses_page.save()

    # Проверяем появление записи
    statuses_page.navigate_to_statuses()
    assert statuses_page.is_status_in_list(status_info=name), (
        "Созданный статус не появился в списке"
    )


@pytest.mark.smoke
def test_2_view_statuses_list(statuses_page_setup):
    statuses_page = statuses_page_setup

    # Проверяем, что таблица загрузилась и ключевые поля отображаются
    assert statuses_page.are_table_headers_visible(), "Ключевые колонки не найдены"

    # Удостоверяемся, что в таблице есть хотя бы одна строка с данными
    rows_count = statuses_page.get_table_rows_count()
    if rows_count == 0:
        statuses_page.create_new_status(name="Backup Status", slug="backup-slug")
        rows_count = statuses_page.get_table_rows_count()

    assert rows_count > 0, "Таблица загрузилась пустой, строк со статусами нет"


@pytest.mark.smoke
def test_3_edit_status(statuses_page_setup):
    statuses_page = statuses_page_setup
    initial_name = "Статус для редактирования"
    updated_name = "Измененный статус"

    # Создаем статус
    statuses_page.create_new_status(name=initial_name, slug="edit-slug")

    # Открываем форму редактирования
    statuses_page.open_status_edit_form(status_info=initial_name)

    # Проверяем данные
    current_values = statuses_page.get_statuses_form_values()
    assert current_values["name"] == initial_name, "В форме открылись неверные данные"

    # Изеняем значения
    statuses_page.fill_status_form(name=updated_name, slug="edit-slug")
    statuses_page.save()

    # Проверяем сохранение в общем списке
    assert statuses_page.is_status_in_list(status_info=updated_name), (
        "Обновленный статус не сохранился"
    )


@pytest.mark.smoke
def test_4_delete_single_status(statuses_page_setup):
    statuses_page = statuses_page_setup
    delete_name = "Статус для удаления"

    # Создаем статус
    statuses_page.create_new_status(name=delete_name, slug="deleted-slug")

    # Выделяем созданный статус
    statuses_page.select_status_in_list(status_info=delete_name)

    # Удаляем и проверяем отсутствие в общем списке
    statuses_page.delete_selected_status()
    statuses_page.wait_for_text_to_disappear(delete_name)
    assert not statuses_page.is_status_in_list(status_info=delete_name), (
        "Статус не удалился из списка"
    )


@pytest.mark.smoke
def test_5_mass_delete_statuses(statuses_page_setup):
    statuses_page = statuses_page_setup
    target_name = "Новый статус"

    # Выделяем все статусы
    statuses_page.select_all_statuses()

    # Удаленяем все статусы
    statuses_page.delete_selected_status()

    # Проверяем, что список статусов пуст после удаления
    statuses_page.wait_for_text_to_disappear(target_name)
    assert not statuses_page.is_status_in_list(status_info=target_name), (
        "Список статусов не очистился полностью"
    )
