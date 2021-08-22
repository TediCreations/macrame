DOCS_DIR = docs/_build

.PHONY: package
package:
	@./setup.py sdist

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

.PHONY: publish
publish: clean package
	@twine upload dist/*

.PHONY: docs
docs:
	@sphinx-apidoc -q --separate --force -o docs/gen/ macrame/ --implicit-namespaces -M --ext-todo
	@sphinx-build -W -a -q -b dirhtml "docs/" "${DOCS_DIR}/dirhtml/"
	@sphinx-build -W -a -q -b html "docs/" "${DOCS_DIR}/html/"
