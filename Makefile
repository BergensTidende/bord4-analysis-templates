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
UV = uv
UV_CACHE_DIR ?= $(PROJECT_DIR)/.uv-cache
UV_RUN = UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) run

#################################################################################
# COMMANDS                                                                      #
#################################################################################

##@ Project Management
.PHONY: sync
sync:  ## Install dependencies with uv
	UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) sync --group analysis

.PHONY: new
new:  ## Create a cell-based Python template from generic-header
	@read -p "Enter file name (with or without .py): " filename; \
	name=$${filename%.py}; \
	cp templates/generic-header.py "templates/$$name.py"; \
	echo "Created templates/$$name.py"

##@ Formatting and linting
.PHONY: format
format: ## Format Python files with Ruff
	@$(UV_RUN) ruff format src tests templates
	@$(UV_RUN) ruff check --fix src tests templates

.PHONY: lint-ruff
lint-ruff: ## Ruff formatter and linter checks
	@$(UV_RUN) ruff format --check src tests templates
	@$(UV_RUN) ruff check src tests templates

.PHONY: lint-mypy
lint-mypy: ## mypy (static-type checker)
	@$(UV_RUN) mypy --config-file pyproject.toml src

.PHONY: lint-mypy-report
lint-mypy-report: ## run mypy & create report
	@$(UV_RUN) mypy --config-file pyproject.toml src --html-report ./mypy_html

lint: lint-ruff lint-mypy ## run all linters

.PHONY: test
test: ## Run tests
	@$(UV_RUN) pytest

.PHONY: build
build: ## Build wheel and source distribution
	@UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) build

.PHONY: check
check: lint test build ## Run all checks and build the package

##@ Releases
.PHONY: clean-dist
clean-dist: ## remove built package artifacts
	@rm -f dist/*.whl dist/*.tar.gz

.PHONY: bump-patch
bump-patch: check ## bump patch version, commit, tag, build and push
	@$(MAKE) clean-dist
	@$(UV_RUN) bump2version patch --verbose
	@$(MAKE) build
	@git push --follow-tags

.PHONY: bump-minor
bump-minor: check ## bump minor version, commit, tag, build and push
	@$(MAKE) clean-dist
	@$(UV_RUN) bump2version minor --verbose
	@$(MAKE) build
	@git push --follow-tags

.PHONY: bump-major
bump-major: check ## bump major version, commit, tag, build and push
	@$(MAKE) clean-dist
	@$(UV_RUN) bump2version major --verbose
	@$(MAKE) build
	@git push --follow-tags

.PHONY: release
release: check ## release package to PyPI (requires UV_PUBLISH_TOKEN)
	@$(MAKE) clean-dist
	@$(MAKE) build
	@UV_CACHE_DIR=$(UV_CACHE_DIR) $(UV) publish
