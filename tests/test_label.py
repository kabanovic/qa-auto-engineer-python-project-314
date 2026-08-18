import pytest
from selenium.webdriver.common.by import By


@pytest.mark.smoke
def test_1_create_label(labels_page_setup):
    labels_page = labels_page_setup
    name = "Фича"

    # Проверяем открытие формы и поля
    labels_page.open_create_form()
    assert "/create" in labels_page.driver.current_url, (
        "URL страницы не изменился на /create"
    )
    assert labels_page.driver.find_element(*labels_page.name_input).is_displayed(), (
        "Поле Название не видно"
    )

    # Заполняем и сохраняем
    labels_page.fill_label_form(name=name)
    labels_page.save()

    # Проверяем появление записи
    labels_page.navigate_to_labels()
    assert labels_page.is_label_in_list(label_info=name), (
        "Созданная метка не появилась в списке"
    )


@pytest.mark.smoke
def test_2_view_labels_list(labels_page_setup):
    labels_page = labels_page_setup

    # Проверяем, что таблица загрузилась и ключевые поля отображаются
    assert labels_page.are_table_headers_visible(), "Ключевые колонки не найдены"

    # Проверяем данные в таблице
    rows_count = labels_page.get_table_rows_count()
    if rows_count == 0:
        labels_page.create_new_label(name="Backup Label")

    rows = labels_page.get_all_table_rows()
    assert len(rows) > 0, "Таблица загрузилась пустой, строк с метками нет"

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        label_data_values = [
            cell.text.strip() for cell in cells[2:] if cell.text.strip() != ""
        ]

        assert len(label_data_values) == 2, (
            f"В строке метки пропущены данные. Данные: {label_data_values}"
        )


@pytest.mark.smoke
def test_3_edit_label(labels_page_setup):
    labels_page = labels_page_setup
    initial_name = "Метка для редактирования"
    updated_name = "Баг"

    # Создаем метку
    labels_page.create_new_label(name=initial_name)

    # Открываем форму редактирования
    labels_page.open_label_edit_form(label_info=initial_name)

    # Проверяем данные
    current_values = labels_page.get_label_form_values()
    assert current_values["name"] == initial_name, "В форме открылись неверные данные"

    # Изеняем значения
    labels_page.fill_label_form(name=updated_name)
    labels_page.save()

    # Проверяем сохранение в общем списке
    labels_page.navigate_to_labels()
    assert labels_page.is_label_in_list(label_info=updated_name), (
        "Обновленная метка не сохранилась"
    )


@pytest.mark.smoke
def test_4_delete_label(labels_page_setup):
    labels_page = labels_page_setup
    delete_name = "Метка для удаления"

    # Создаем метку
    labels_page.create_new_label(name=delete_name)

    # Выделяем созданную метку
    labels_page.select_label_in_list(label_info=delete_name)

    # Удаляем и проверяем отсутствие в общем списке
    labels_page.delete_selected_label()
    labels_page.wait_for_text_to_disappear(delete_name)
    assert not labels_page.is_label_in_list(label_info=delete_name), (
        "Метка не удалилась из списка"
    )
