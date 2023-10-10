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
	@echo ""
	@echo "🛠  INSTALL & RELEASE"
	@echo "---------------------------------------------------------------------"
	@echo "  install             Install library to site-packages"
	@echo "  release             Build & push package to PyPI"
	@echo "  clean               Clean build/install artifacts"

sec:
	@bandit -r yclients_aio_client

lint:
	@black yclients_aio_client tests --color --diff --check

lint-apply:
	@black yclients_aio_client tests

test:
	@pytest -vv --cov=yclients_aio_client

tests: test

test-no-cov:
	@pytest -v

init:
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt
	@pre-commit install --install-hooks -f

pre-commit:
	@pre-commit run --all-files

clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -f {} +
	find . -name '.DS_Store' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

dist:
	python3 setup.py sdist
	python3 setup.py bdist_wheel

release: dist
	@make dist
	python3 -m twine upload --repository pypi dist/*

install: clean
	python3 setup.py install
