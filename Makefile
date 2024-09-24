# Variables
DOCKER_COMPOSE = docker compose -f local.yml
DJANGO_MANAGE = $(DOCKER_COMPOSE) run --rm api python manage.py
DB_CONTAINER = postgres

# Default Target (optional)
.DEFAULT_GOAL := help

# Help - lists the available commands
help:
	@echo "Available commands:"
	@echo "  make build        - Build the Docker containers"
	@echo "  make up           - Start the services"
	@echo "  make down         - Stop the services"
	@echo "  make backup-db    - Backup the PostgreSQL database"
	@echo "  make restore-db   - Restore the PostgreSQL database"
	@echo "  make migrate      - Run Django migrations"
	@echo "  make createsuper  - Create Django superuser"
	@echo "  make shell        - Open Django shell"
	@echo "  make logs         - Tail logs from all services"
	@echo "  make test         - Run Django tests"
	@echo "  make collectstatic - Collect static files"

# Docker Commands
build:
	$(DOCKER_COMPOSE) up --build -d --remove-orphans

up:
	$(DOCKER_COMPOSE) up -d

down:
	$(DOCKER_COMPOSE) down

down-v:
	$(DOCKER_COMPOSE) down -v

logs:
	$(DOCKER_COMPOSE) logs 

logs-api:
	$(DOCKER_COMPOSE) logs api

# Django Management Commands
makemigrations:
	$(DJANGO_MANAGE) makemigrations

migrate:
	$(DJANGO_MANAGE) migrate

createsuper:
	$(DJANGO_MANAGE) createsuperuser

shell:
	$(DJANGO_MANAGE) shell

collectstatic:
	$(DJANGO_MANAGE) collectstatic --no-input --clear

test:
	$(DJANGO_MANAGE) test

volume:
	docker volume inspect medium-clone_local_postgres_data

# Database Commands
medium-db:
	$(DOCKER_COMPOSE) exec $(DB_CONTAINER) psql --username=xen --dbname=medium

backup-db:
	$(DOCKER_COMPOSE) exec $(DB_CONTAINER) backup

restore-db:
	$(DOCKER_COMPOSE) exec $(DB_CONTAINER) restore backup_YYYY_MM_DD.sql.gz

# Linter Commands
flake8:
	$(DOCKER_COMPOSE) exec api flake8 .

block-check:
	$(DOCKER_COMPOSE) exec api black --check --exclude=migrations .

block-diff:
	$(DOCKER_COMPOSE) exec api black --diff --exclude=migrations .

black:
	$(DOCKER_COMPOSE) exec api black --exclude=migrations .

isort-check:
	$(DOCKER_COMPOSE) exec api isort . --check-only --skip .venv --skip migrations

isort-diff:
	$(DOCKER_COMPOSE) exec api isort . --diff --skip .venv --skip migrations

isort:
	$(DOCKER_COMPOSE) exec api isort . --skip .venv --skip migrations

# Add More Commands As Needed...
