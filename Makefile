.DEFAULT_GOAL := help

help:
	@echo "🪄  PREPARE ENVIRONMENT"
	@echo "---------------------------------------------------------------------"
	@echo "  init                Install all python requirements"
	@echo "  pre-commit          Install pre-commit hooks"
	@echo ""
	@echo "⚙️  DEVELOPMENT"
	@echo "---------------------------------------------------------------------"
	@echo "  test                Run tests (pytest)"
	@echo "  test-no-cov         Run tests (pytest) without coverage report"
	@echo "  lint                Check python syntax & style by black"
	@echo "  lint-apply          Apply black linter (autoformat)"
	@echo "  sec                 Security linter (bandit)"

sec:
	@bandit -r yclients_aio_client

lint:
	@black yclients_aio_client tests --color --diff --check

lint-apply:
	@black yclients_aio_client tests

test:
	@pytest -vv --cov=src

tests: test

test-no-cov:
	@pytest -v

init:
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt
	@pre-commit install

pre-commit:
	@pre-commit run --all-files
