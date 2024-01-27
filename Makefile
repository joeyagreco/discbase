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