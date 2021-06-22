# For more information on the following see http://clarkgrubb.com/makefile-style-guide
MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help
.DELETE_ON_ERROR:
.SUFFIXES:

COMPOSE_CMD=docker-compose
RUN_DJANGO = $(COMPOSE_CMD) run --rm django
HELP_FIRST_COL_LENGTH := 23
ARGS=$(filter-out $@,$(MAKECMDGOALS))

# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)
TARGET_MAX_CHAR_NUM := 23

.PHONY: help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-$(TARGET_MAX_CHAR_NUM)s$(RESET)$(GREEN)%s$(RESET)\n", $$1, $$2}'
	@echo ''

.PHONY: clean
clean: remove_py_cache remove_coverage_data ## Remove build files, python cache files and test coverage data
	rm -rf docs/_build/
	rm -rf public/static/

.PHONY: build
build: ## Docker-compose build and pipchecker
	$(COMPOSE_CMD) build
	$(RUN_DJANGO) python manage.py pipchecker

.PHONY: up
up: ## Docker-compose up
	$(COMPOSE_CMD) up

.PHONY: down
down: ## Docker-compose down
	$(COMPOSE_CMD) down

.PHONY: restart
restart: ## Docker-compose restart
	$(COMPOSE_CMD) restart

.PHONY: makemigrations
makemigrations: ## Creates new migrations based on models changes
	$(RUN_DJANGO) python manage.py makemigrations --no-header

.PHONY: migrate
migrate: ## Synchronizes the database state with current set of models and migrations
	$(RUN_DJANGO) python manage.py migrate

.PHONE: data_reset
data_reset: ## Reset database
	echo 'yes' | $(RUN_DJANGO) python manage.py reset_db

.PHONY: shell
shell: ## Run Django shell
	$(RUN_DJANGO) python manage.py shell_plus

.PHONY: shell_sql
shell_sql: ## Run Django shell with printing SQL
	$(RUN_DJANGO) python manage.py shell_plus --print-sql

.PHONY: test_mypy
test_mypy: ## Run mypy
	$(RUN_DJANGO) mypy --install-types .

.PHONY: test_pytest
test_pytest: ## Run pytest
	$(RUN_DJANGO) pytest --cov --cov-report term-missing:skip-covered

.PHONY: coverage
coverage: ## Generate html coverage report
	$(RUN_DJANGO) coverage html

.PHONY: coverage_open
coverage_open: ## Generate and open html coverage report
	$(RUN_DJANGO) coverage html && open htmlcov/index.html

.PHONY: test
test:  test_mypy test_pytest ## Run pytest and mypy

.PHONY: format_imports
format_imports: ## Format Python imports with isort
	$(RUN_DJANGO) isort .

.PHONY: format_py
format_py: ## Format Python code format with black
	$(RUN_DJANGO) black .

.PHONY: format
format: format_imports format_py ## Format Python code and Python imports

.PHONY: lint
lint: ## Lint Python code with flake8 and pylint
	$(RUN_DJANGO) flake8
	$(RUN_DJANGO) pylint config/ apps/

.PHONY: all
all: test format lint ## Run all testing, formating and linting tools

.PHONY: remove_coverage_data
remove_coverage_data: ## Remove Django test coverage data
	rm -f .coverage
	rm -rf htmlcov

.PHONY: remove_py_cache
remove_py_cache: ## Remove cached Python bytecode
	find . -name "*.pyc" | xargs rm -rf
	find . -name "*.pyo" | xargs rm -rf
	find . -name "__pycache__" -type d | xargs rm -rf

.PHONY: check
check: ## Inspect the entire Django project for common problems
	$(RUN_DJANGO) python manage.py check

.PHONY: check_deploy
check_deploy: ## Inspect the project for deployment
	docker-compose run --rm django python manage.py check --deploy --settings=config.settings.staging

.PHONY: manage
manage: ## Saves parsed results to database
	$(RUN_DJANGO) python manage.py ${ARGS}
