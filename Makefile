install:
	uv sync

build:
	uv build

lint:
	uv run ruff check validator tests

lint-fix:
	uv run ruff check --fix validator tests

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=validator --cov-report=xml --cov-report=term

check: lint test

.PHONY: install build lint lint-fix test test-coverage check
