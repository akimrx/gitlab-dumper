.PHONY: clean clean-build clean-pyc dist help test tests sessions
.DEFAULT_GOAL := help

help:
	@echo "🪄  PREPARE ENVIRONMENT"
	@echo "---------------------------------------------------------------------"
	@echo "  init                Install all python requirements"
	@echo "  pre-commit          Install pre-commit hooks"
	@echo ""
	@echo "👀  CHECK"
	@echo "---------------------------------------------------------------------"
	@echo "  test                Run tests (pytest)"
	@echo "  test-no-cov         Run tests (pytest) without coverage report"
	@echo "  pylint              Check python syntax & style by pylint"
	@echo "  lint                Check python syntax via Flake8"
	@echo "  mypy                Check typing annotation via MyPy"
	@echo "  black               Check python syntax & style by black"
	@echo "  black-apply         Apply black linter (autoformat)"
	@echo "  sec                 Security linter (bandit)"
	@echo ""
	@echo "🛠  INSTALL & RELEASE"
	@echo "---------------------------------------------------------------------"
	@echo "  install             Install library to site-packages"
	@echo "  release             Build & push package to PyPI"
	@echo "  build               Build package"
	@echo "  build-docker        Build dev docker image"
	@echo "  clean               Clean build/install artifacts"


clean: clean-build clean-pyc

clean-build:
	rm -rf build/
	rm -rf dist/
	rm -rf .eggs/
	find . -name '*.egg-info' -exec rm -rf {} +
	find . -name '*.egg' -exec rm -rf {} +
	find . -name '.DS_Store' -exec rm -f {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

test:
	@pytest -vv --cov=src

tests: test

test-no-cov:
	@pytest -v

lint:
	@flake8 --config=setup.cfg --max-line=119

pylint:
	@pylint --max-line-length=119 --rcfile=setup.cfg src

mypy:
	@mypy src

black:
	@black src/* --color --diff --check

black-apply:
	@black src/*

sec:
	@bandit -r src

build:
	@python3 setup.py sdist bdist_wheel

install: clean
	@python3 setup.py install

release: build
	@make build
	@python3 -m twine upload --repository pypi dist/*

init:
	@pip3 install -r requirements.txt
	@pip3 install -r requirements-dev.txt || true
