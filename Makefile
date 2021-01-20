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


build: copy-ssh-keys

bash: copy-ssh-keys