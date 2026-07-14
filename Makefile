.PHONY: install test test-unit test-integration coverage lint format quality security

install:
	python -m pip install -r requirements-dev.txt

test:
	pytest

test-unit:
	pytest tests/test_domain.py

test-integration:
	pytest tests/test_api.py

coverage:
	pytest --cov-report=term-missing --cov-report=html --cov-report=xml

lint:
	ruff check app tests
	ruff format --check app tests

format:
	ruff check --fix app tests
	ruff format app tests

security:
	bandit -r app -q

quality: lint test security
.PHONY: compose-up compose-down kind-up kind-down deploy-local k8s-status

compose-up:
	docker compose up --build

compose-down:
	docker compose down -v

kind-up:
	./scripts/kind-up.sh

kind-down:
	./scripts/kind-down.sh

deploy-local:
	./scripts/deploy-local.sh

k8s-status:
	kubectl get pods,svc,ingress,hpa -n oficina
