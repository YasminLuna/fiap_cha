.PHONY: install test lint up down
install:
	pip install -r requirements-dev.txt
test:
	pytest
lint:
	ruff check app tests
up:
	cp -n .env.example .env || true
	docker compose up --build -d
down:
	docker compose down
