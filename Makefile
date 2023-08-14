.PHONY: tests
tests: unittests mypy lint

.PHONY: unittests
unittests:
	poetry run pytest --cov=syncer .

.PHONY: lint
lint:
	poetry run pylint --max-line-length=119 syncer

.PHONY: mypy
mypy:
	poetry run mypy syncer

