PYTHON ?= python

.PHONY: install lint format typecheck test check run

install:
	$(PYTHON) -m pip install -e ".[dev]"

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src

test:
	pytest

check: lint typecheck test

run:
	uvicorn start_os.main:app --reload --host 0.0.0.0 --port 8000
