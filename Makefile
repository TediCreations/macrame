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
	@echo "Done"

.PHONY: publish
publish: clean package
	twine upload dist/*
