.PHONY: run
run: 
	python3.10 discbase/run.py

.PHONY: deps
deps:
	@brew install postgresql
	@python3.10 -m pip install -r requirements.dev.txt
	@python3.10 -m pip install -r requirements.txt


.PHONY: fmt
fmt:
	@black --config=pyproject.toml .
	@autoflake --config=pyproject.toml .
	@isort .

.PHONY: pkg-build
pkg-build:
	@rm -rf build
	@rm -rf dist
	@python3 setup.py sdist bdist_wheel

.PHONY: pkg-test
pkg-test:
	@python3 -m twine upload testpypi dist/*

.PHONY: pkg-prod
pkg-prod:
	@python3 -m twine upload dist/*