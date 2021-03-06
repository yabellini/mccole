SRC=mccole

# Show help by default.
.DEFAULT_GOAL := help

## help: show available commands
.PHONY: help
help:
	@grep -h -E '^##' ${MAKEFILE_LIST} | sed -e 's/## //g' | column -t -s ':'

## test: run unit tests
.PHONY: test
test:
	@pytest tests

## manual: run on-disk tests
.PHONY: manual
manual:
	@for dir in manual/*; do echo $$dir; python -m mccole -C $$dir -g html.yml; done

## install: build package and install locally
.PHONY: install
install:
	python setup.py install

## coverage: run available tests and report coverage
.PHONY: coverage
coverage:
	@coverage run -m pytest
	@coverage html

## docs: build documentation
.PHONY: docs
docs:
	@mkdocs build

## lint: run software quality checks
.PHONY: lint
lint:
	@-flake8
	@-isort --check .
	@-black --check .
	@-pydocstyle --convention=google --count ${SRC}

## reformat: reformat code in place
.PHONY: reformat
reformat:
	@isort .
	@black .

## clean: remove junk files
.PHONY: clean
clean:
	@find . -name '*~' -exec rm {} \;
	@rm -rf $$(find . -name __pycache__ -print)
	@find . -name .DS_Store -exec rm {} \;
	@rm -rf htmlcov
	@rm -rf manual/*/tmp
