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
UV = uv
UV_CACHE_DIR ?= $(PROJECT_DIR)/.uv-cache
UV_RUN = UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run

#################################################################################
# COMMANDS                                                                      #
#################################################################################

##@ Project Management
.PHONY: sync
sync:  ## Install dependencies with uv
	UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) sync

.PHONY: lab
lab:  ## Run Jupyter lab
	$(UV_RUN) jupyter lab

.PHONY: new
new:  ## Create new template file from generic-header
	@read -p "Enter file name for the new template:" filename; \
	cp templates/generic-header.ipynb templates/$$filename.ipynb; \
	echo "Created templates/$$filename.ipynb"

##@ Formatting and linting
.PHONY: format
format: ## Format Python files and notebooks with Ruff
	@$(UV_RUN) ruff format src templates
	@$(UV_RUN) ruff check --fix src templates

.PHONY: lint-ruff
lint-ruff: ## Ruff formatter and linter checks
	@$(UV_RUN) ruff format --check src templates
	@$(UV_RUN) ruff check src templates

.PHONY: lint-mypy
lint-mypy: ## mypy (static-type checker)
	@$(UV_RUN) mypy --config-file pyproject.toml src

.PHONY: lint-mypy-report
lint-mypy-report: ## run mypy & create report
	@$(UV_RUN) mypy --config-file pyproject.toml src --html-report ./mypy_html

lint: lint-ruff lint-mypy ## run all linters
