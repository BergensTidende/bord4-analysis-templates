#################################################################################
# SELF DOCUMENTING HELP                                                                       #
#################################################################################

.DEFAULT_GOAL := help
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.project_name }}
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

##@ Project Management
.PHONY: lab
lab:  ## Run Jupyter lab
	poetry run jupyter lab

.PHONY: new
new:  ## Create new template file from generic-header
	@read -p "Enter file name for the new template:" filename; \
	cp templates/generic-header.ipynb templates/$$filename.ipynb; \
	echo "Created templates/$$filename.ipynb"

##@ Formatting
.PHONY: format-black
format-black: ## black (code formatter)
	@poetry run black templates
	@poetry run black src

.PHONY: format-isort
format-isort: ## isort (import formatter)
	@poetry run isort src

.PHONY: format
format: format-black format-isort ## run all formatters

##@ Linting
.PHONY: lint-black
lint-black: ## black in linting mode
	@poetry run black templates --check
	@poetry run black src --check

.PHONY: lint-isort
lint-isort: ## isort in linting mode
	@poetry run isort src --check

.PHONY: lint-flake8
lint-flake8: ## flake8 (linter)
	@poetry run flake8 src

.PHONY: lint-mypy
lint-mypy: ## mypy (static-type checker)
	@poetry run mypy --config-file pyproject.toml src

.PHONY: lint-mypy-report
lint-mypy-report: ## run mypy & create report
	@poetry run mypy --config-file pyproject.toml src --html-report ./mypy_html

lint: lint-black lint-isort lint-flake8 lint-mypy ## run all linters


