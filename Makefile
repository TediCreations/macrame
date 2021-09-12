DOCS_DIR = docs/_build

.PHONY: all
all: checks package
	:

.PHONY: checks
checks: lint test docs
	:

.PHONY: package
package:
	@./setup.py sdist

.PHONY: publish
publish: clean package
	@twine upload dist/*

.PHONY: docs
docs:
	@sphinx-apidoc -q --separate --force -o docs/gen/ macrame/ --implicit-namespaces -M --ext-todo
	@sphinx-build -W -a -q -b dirhtml "docs/" "${DOCS_DIR}/dirhtml/"
	@sphinx-build -W -a -q -b html "docs/" "${DOCS_DIR}/html/"

.PHONY: test
test:
	@python -m pytest

.PHONY: lint
lint:
	@pylint macrame

.PHONY: clean
clean:
	@rm -rf MANIFEST
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf .eggs
	@rm -rf .pytest_cache
	@py3clean .
	@rm -rf ${DOCS_DIR}
	@echo "Done"
