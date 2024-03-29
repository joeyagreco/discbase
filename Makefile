SPEEDTEST_COUNT = 10

.PHONY: run
run: 
	python3.10 discbase/run.py

.PHONY: deps
deps:
	@python3.10 -m pip install -r requirements.dev.txt
	@python3.10 -m pip install -r requirements.txt


.PHONY: fmt
fmt:
	@black --config=pyproject.toml .
	@autoflake --config=pyproject.toml .
	@isort .

.PHONY: fmt-check
fmt-check:
	@black --config=pyproject.toml . --check
	@autoflake --config=pyproject.toml . --check
	@isort . --check-only

.PHONY: speedtest
speedtest:
	@python3.10 speedtest.py $(SPEEDTEST_COUNT)

.PHONY: test-unit
test-unit:
	@pytest test_unit/

.PHONY: test-e2e
test-e2e:
	@pytest test_e2e/

.PHONY: test-all
test-all:
	@$(MAKE) test-unit
	@$(MAKE) test-e2e

.PHONY: pkg-build
pkg-build:
	@rm -rf build
	@rm -rf dist
	@python3 setup.py sdist bdist_wheel

.PHONY: pkg-test
pkg-test:
	@python3 -m twine upload --repository testpypi dist/*


.PHONY: pkg-prod
pkg-prod:
	@python3 -m twine upload dist/*