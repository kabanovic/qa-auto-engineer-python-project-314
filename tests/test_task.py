import pytest


@pytest.mark.smoke
def test_1_create_task(tasks_page_setup):
    tasks_page = tasks_page_setup
    title = "Task_Create_QA"

    # Проверяем открытие формы
    tasks_page.open_create_form()
    assert "/create" in tasks_page.driver.current_url, (
        "URL страницы не изменился на /create"
    )
    assert tasks_page.driver.find_element(*tasks_page.title_input).is_displayed(), (
        "Поле Title не отображается"
    )
    assert tasks_page.driver.find_element(*tasks_page.status_select).is_displayed(), (
        "Поле Status не отображается"
    )
    assert tasks_page.driver.find_element(*tasks_page.assignee_select).is_displayed(), (
        "Поле Assignee не отображается"
    )

    # Заполняем обязательные поля
    tasks_page.fill_task_form(
        title=title,
        status_text="Draft",
        assignee_text="john@google.com",
        label="feature",
        content="This is a test description for QA validation",
    )
    tasks_page.save()

    # Убеждаемся, что она появилась на доске в нужной колонке
    tasks_page.navigate_to_tasks()
    assert tasks_page.is_task_in_column(task_info=title, column_name="Draft"), (
        "Задача не появилась в колонке"
    )


@pytest.mark.smoke
def test_2_view_and_filter_tasks(tasks_page_setup):
    tasks_page = tasks_page_setup
    target_task = "Task_Target_All_Pass"
    wrong_status_task = "Task_Wrong_Status"
    wrong_assignee_task = "Task_Wrong_Assignee"
    wrong_label_task = "Task_Wrong_Label"

    initial_count = tasks_page.get_tasks_count()
    if initial_count == 0:
        tasks_page.create_new_task_shortcut(
            title="test", status_text="To Publish", assignee_text="jack@yahoo.com"
        )
        initial_count = tasks_page.get_tasks_count()

    # Удостоверяемся, что записи на доске загрузились и отображаются
    assert initial_count > 0, (
        "Канбан-доска загрузилась пустой, задачи не отображаются при открытии"
    )

    # Создаем тестовые записи на доске
    if not tasks_page.is_task_in_list(task_info=target_task):
        tasks_page.create_new_task_shortcut(
            title=target_task,
            status_text="Draft",
            assignee_text="john@google.com",
            label="feature",
        )
    if not tasks_page.is_task_in_list(task_info=wrong_status_task):
        tasks_page.create_new_task_shortcut(
            title=wrong_status_task,
            status_text="To Be Fixed",
            assignee_text="john@google.com",
            label="feature",
        )
    if not tasks_page.is_task_in_list(task_info=wrong_assignee_task):
        tasks_page.create_new_task_shortcut(
            title=wrong_assignee_task,
            status_text="Draft",
            assignee_text="jane@gmail.com",
            label="feature",
        )
    if not tasks_page.is_task_in_list(task_info=wrong_label_task):
        tasks_page.create_new_task_shortcut(
            title=wrong_label_task,
            status_text="Draft",
            assignee_text="john@google.com",
            label="bug",
        )

    # Включаем фильтр по статусу
    tasks_page.apply_status_filter(status_text="Draft")
    tasks_page.wait_for_text_to_disappear(wrong_status_task)

    assert tasks_page.is_task_in_list(task_info=target_task), (
        "Фильтр статуса скрыл нужную задачу"
    )
    assert not tasks_page.is_task_in_list(task_info=wrong_status_task), (
        "Фильтр статуса НЕ скрыл задачу 'To Be Fixed'!"
    )
    assert tasks_page.is_task_in_list(task_info=wrong_assignee_task), (
        "Фильтр статуса скрыл нужную задачу"
    )
    assert tasks_page.is_task_in_list(task_info=wrong_label_task), (
        "Фильтр статуса скрыл нужную задачу"
    )

    # Добавляем фильтр по исполнителю
    tasks_page.apply_assignee_filter(assignee_text="john@google.com")
    tasks_page.wait_for_text_to_disappear(wrong_assignee_task)

    assert tasks_page.is_task_in_list(task_info=target_task), (
        "Фильтр исполнителя скрыл нужную задачу"
    )
    assert not tasks_page.is_task_in_list(task_info=wrong_status_task)
    assert not tasks_page.is_task_in_list(task_info=wrong_assignee_task), (
        "Фильтр исполнителя НЕ скрыл чужую задачу!"
    )
    assert tasks_page.is_task_in_list(task_info=wrong_label_task)

    # Добавляем фильтр по метке
    tasks_page.apply_label_filter(label_text="feature")
    tasks_page.wait_for_text_to_disappear(wrong_label_task)

    assert tasks_page.is_task_in_list(task_info=target_task), (
        "Фильтр меток скрыл нужную задачу"
    )
    assert not tasks_page.is_task_in_list(task_info=wrong_status_task)
    assert not tasks_page.is_task_in_list(task_info=wrong_assignee_task)
    assert not tasks_page.is_task_in_list(task_info=wrong_label_task), (
        "Фильтр меток НЕ скрыл задачу с другой меткой!"
    )


@pytest.mark.smoke
def test_3_edit_task(tasks_page_setup):
    tasks_page = tasks_page_setup
    initial_title = "Task_To_Edit"
    updated_title = "Task_Has_Been_Updated"

    # Создаем новую задачу
    tasks_page.create_new_task_shortcut(
        title=initial_title, status_text="Draft", assignee_text="john@google.com"
    )

    # Открываем форму редактирования
    tasks_page.open_task_edit_form(task_info=initial_title)

    # Проверяем данные
    current_values = tasks_page.get_task_form_values()
    assert current_values["title"] == initial_title, (
        "В форме редактирования открылись неверные данные"
    )

    # Изменяем знечение
    tasks_page.fill_task_form(
        title=updated_title,
        status_text="Draft",
        assignee_text="john@google.com",
        label="bug",
        content="Updated test description for validation",
    )
    tasks_page.save()

    # Проверяем отображение обновленных изменений
    assert tasks_page.is_task_in_list(task_info=updated_title), (
        "Обновленная задача не появилась на доске"
    )


@pytest.mark.smoke
def test_4_move_task_between_columns(tasks_page_setup):
    tasks_page = tasks_page_setup
    title = "Task_To_Move"
    create_status = "Draft"
    new_status = "Published"

    # Создаем задачу
    tasks_page.create_new_task_shortcut(
        title=title, status_text=create_status, assignee_text="john@google.com"
    )

    # Меняем у задачи статус
    tasks_page.change_task_status_via_edit(task_info=title, new_status_text=new_status)

    # Проверяем, что задача переместилась в столбец с указазанным статусом
    assert tasks_page.is_task_in_column(task_info=title, column_name=new_status), (
        f"Задача не переместилась в столбец {new_status}"
    )


@pytest.mark.smoke
def test_5_delete_task(tasks_page_setup):
    tasks_page = tasks_page_setup
    title = "Task_To_Delete"

    # Создаем задачу
    tasks_page.create_new_task_shortcut(
        title=title, status_text="To Publish", assignee_text="john@google.com"
    )

    # Удаляем задачу
    tasks_page.delete_task(task_info=title)

    # Убеждаемся, что она полностью исчезла с доски
    assert not tasks_page.is_task_in_list(task_info=title), (
        "Задача не исчезла после удаления"
    )
