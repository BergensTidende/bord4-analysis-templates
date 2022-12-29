#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROJECT_NAME = {{ cookiecutter.project_name }}
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Run Jupyter lab
.PHONY: lab
lab:
	poetry run jupyter lab

## Create new template file from generic-header
.PHONY: new
new:
	@read -p "Enter file name for the new template:" filename; \
	cp templates/generic-header.ipynb templates/$$filename.ipynb; \
	echo "Created templates/$$filename.ipynb"

##@ Formatting
.PHONY: format-black
format-black: ## black (code formatter)
	@black src

.PHONY: format-isort
format-isort: ## isort (import formatter)
	@isort src

.PHONY: format
format: format-black format-isort ## run all formatters

##@ Linting
.PHONY: lint-black
lint-black: ## black in linting mode
	@black . --check

.PHONY: lint-isort
lint-isort: ## isort in linting mode
	@isort src --check

.PHONY: lint-flake8
lint-flake8: ## flake8 (linter)
	@flake8 src

.PHONY: lint-mypy
lint-mypy: ## mypy (static-type checker)
	@mypy --config-file pyproject.toml src

.PHONY: lint-mypy-report
lint-mypy-report: ## run mypy & create report
	@mypy --config-file pyproject.toml src --html-report ./mypy_html

lint: lint-black lint-isort lint-flake8 lint-mypy ## run all linters


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: help
help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
