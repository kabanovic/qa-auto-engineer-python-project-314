start:
	docker run --rm -p 5173:5173 hexletprojects/qa_auto_python_testing_kanban_board_project_ru_app

test:
	APP_BASE_URL=http://localhost:5173 uv run pytest -k smoke

lint:
	uv run ruff check --fix
	uv run ruff format