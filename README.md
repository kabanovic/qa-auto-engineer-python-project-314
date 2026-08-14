### Hexlet tests and linter status:
[![Actions Status](https://github.com/kabanovic/qa-auto-engineer-python-project-314/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kabanovic/qa-auto-engineer-python-project-314/actions)

# Автотесты для Канбан-доски

Проект содержит автотесты для веб-приложения «Канбан-доска».

---

## 📊 Покрытие тестами

* **Авторизация (`test_auth.py`)** 
* **Задачи (`test_tasks.py`)** 
* **Метки (`test_labels.py`)** 
* **Статусы (`test_statuses.py`)** 
* **Пользователи (`test_users.py`)** 

---

## Как запустить тесты локально

Для работы проекта необходимы установленные **Docker** и менеджер зависимостей **uv**.

### 1. Установка зависимостей
Перед первым запуском синхронизируйте виртуальное окружение:
```bash
uv sync
```
Чтобы проверить код на соответствие стандартам PEP 8, запустите:
```bash
make lint
```

### 2. Запуск тестируемого приложения
В первом терминале запустите Docker-контейнер с приложением Хекслета:
```bash
make start
```

### 3. Запуск автотестов
Во втором терминале запустите прогон smoke-тестов:
```bash
make test
```
