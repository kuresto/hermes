#!/bin/bash
PYVERSION=3.9
ENVIRONMENT=dev


help: ## make [target]
	@echo ""
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo

clean: ## cleans the project from python cache files and logs.
	find . -name "*.pyc" -exec rm -rf {} \;
	rm -rf *.log

copy-ssh-keys: ## copy the ssh keys for github private projects
	mkdir -p ./.keys/
	cp -r ~/.ssh/* ./.keys/

setup-dev: copy-ssh-keys  ## Prepares your project folder for development
	python${PYVERSION} -m venv venv
	( \
		source venv/bin/activate; \
		pip install -r requirements/development.txt; \
		echo "Setup completed, now please run `source venv/bin/activate` "; \
	)


local-server:  ## Starts a uvicorn server for this service
	uvicorn hermes.app:app --reload


migration:  ## Generates a migration based on model changes
	alembic revision --autogenerate

migrate:  ## Migrates the database
	alembic upgrade head

build:  ## Build all the docker images for local development
	docker-compose --file docker/development/docker-compose.yml build --no-cache

up:  ## Up all docker images
	docker-compose --file docker/development/docker-compose.yml up -d

setup-dev: copy-ssh-keys build up migrate  ## Prepares your project folder for development
	python${PYVERSION} -m venv venv
	( \
		source venv/bin/activate; \
		pip install -r requirements/development.txt; \
		echo "Setup completed, now please run `source venv/bin/activate` "; \
	)
